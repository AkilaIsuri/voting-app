// worker/Program.cs
using System;
using System.Threading;
using StackExchange.Redis;
using Npgsql;

class Program
{
    static void Main(string[] args)
    {
        var redisHost = Environment.GetEnvironmentVariable("REDIS_HOST") ?? "redis";
        var redisPort = Environment.GetEnvironmentVariable("REDIS_PORT") ?? "6379";
        var pgHost = Environment.GetEnvironmentVariable("POSTGRES_HOST") ?? "db";
        var pgUser = Environment.GetEnvironmentVariable("POSTGRES_USER") ?? "postgres";
        var pgPass = Environment.GetEnvironmentVariable("POSTGRES_PASSWORD") ?? "postgres";
        var pgDb   = Environment.GetEnvironmentVariable("POSTGRES_DB") ?? "votes";

        var redisConnStr = $"{redisHost}:{redisPort}";
        Console.WriteLine($"Connecting to Redis at {redisConnStr}");
        var redis = ConnectionMultiplexer.Connect(redisConnStr);
        var db = redis.GetDatabase();

        var pgConnStr = $"Host={pgHost};Username={pgUser};Password={pgPass};Database={pgDb}";
        Console.WriteLine($"Connecting to Postgres at {pgHost}");
        // Ensure table exists
        using (var conn = new NpgsqlConnection(pgConnStr))
        {
            conn.Open();
            string createSql = @"
                CREATE TABLE IF NOT EXISTS results (
                    option TEXT PRIMARY KEY,
                    count INTEGER NOT NULL
                );";
            using (var cmd = new NpgsqlCommand(createSql, conn))
            {
                cmd.ExecuteNonQuery();
            }
            conn.Close();
        }

        Console.WriteLine("Worker started. Polling Redis list 'votes' ...");
        while (true)
        {
            try
            {
                // BLPOP would be ideal, but using blocking pop isn't directly in StackExchange,
                // so we poll with a short sleep - acceptable for demo.
                var value = db.ListLeftPop("votes");
                if (value.IsNullOrEmpty)
                {
                    Thread.Sleep(500); // sleep and poll again
                    continue;
                }

                var option = value.ToString();
                Console.WriteLine($"Got vote: {option}");

                using (var conn = new NpgsqlConnection(pgConnStr))
                {
                    conn.Open();
                    // Upsert (insert or increment)
                    string upsert = @"
                        INSERT INTO results (option, count)
                        VALUES (@option, 1)
                        ON CONFLICT (option)
                        DO UPDATE SET count = results.count + 1;
                    ";
                    using (var cmd = new NpgsqlCommand(upsert, conn))
                    {
                        cmd.Parameters.AddWithValue("option", option);
                        cmd.ExecuteNonQuery();
                    }
                    // Also keep a quick Redis cache of counts for frontend quick read
                    using (var cmd2 = new NpgsqlCommand("SELECT count FROM results WHERE option=@option", conn))
                    {
                        cmd2.Parameters.AddWithValue("option", option);
                        var res = cmd2.ExecuteScalar();
                        if (res != null)
                        {
                            db.StringSet($"count:{option}", res.ToString());
                        }
                    }
                    conn.Close();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Worker error: " + ex.Message);
                Thread.Sleep(1000);
            }
        }
    }
}
