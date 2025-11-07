# worker/Dockerfile
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src
COPY . .
RUN dotnet publish -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/runtime:7.0
WORKDIR /app
COPY --from=build /app/publish .
ENV DOTNET_URLS=http://0.0.0.0:80
ENTRYPOINT ["dotnet", "worker.dll"]
