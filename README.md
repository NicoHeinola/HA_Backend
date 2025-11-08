# Home Assistant Docker Setup

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system
- Linux, macOS, or Windows with Docker Desktop
- At least 2GB of free disk space

### Setup Instructions

1. **Configure Environment Variables**

   ```bash
   # Edit the .env file and set secure passwords
   nano .env
   ```

2. **Start Home Assistant (Basic Setup)**

   ```bash
   docker-compose up -d
   ```

   This starts only the Home Assistant container on port 8123.

3. **Start with Optional Services**

   ```bash
   # Include MariaDB for history database
   docker-compose --profile database up -d

   # Include InfluxDB for metrics
   docker-compose --profile metrics up -d

   # Include all services
   docker-compose --profile database --profile metrics up -d
   ```

4. **Access Home Assistant**
   - Open your browser and go to: `http://localhost:8123`
   - Complete the onboarding wizard
   - Create your admin user account

### Useful Commands

```bash
# View logs
docker-compose logs -f home-assistant

# Stop containers
docker-compose down

# Restart Home Assistant
docker-compose restart home-assistant

# Update to latest version
docker-compose pull
docker-compose up -d

# Access Home Assistant shell
docker-compose exec home-assistant bash

# Check container status
docker-compose ps
```

### Configuration

#### Time Zone

Edit the `TZ` variable in `.env` to match your timezone (e.g., `America/New_York`, `Europe/London`, `Asia/Tokyo`)

#### Database (Optional)

To enable MariaDB for storing history:

1. Set secure passwords in `.env`
2. Start with: `docker-compose --profile database up -d`
3. Configure in Home Assistant:
   - Settings → Devices & Services → Integrations → Recorder
   - Add MariaDB connection details

#### InfluxDB (Optional)

For time-series metrics:

1. Set passwords in `.env`
2. Start with: `docker-compose --profile metrics up -d`
3. Configure in Home Assistant for long-term statistics

### Volumes

- `./config/` - Home Assistant configuration files (persistent)
- `./db_data/` - MariaDB data (persistent)
- `./influxdb_data/` - InfluxDB data (persistent)

### Security Tips

1. **Change default passwords in `.env`** before first run
2. **Use strong passwords** for database and InfluxDB
3. **Enable authentication** in Home Assistant
4. **Keep Docker images updated** regularly
5. **Use firewall** to restrict access to port 8123
6. **Consider reverse proxy** (nginx) for HTTPS

### Troubleshooting

**Port already in use:**

```bash
# Change port in docker-compose.yml
# Change line: "8123:8123" to "8124:8123" for port 8124
```

**Permission denied accessing config:**

```bash
sudo chown -R 1000:1000 ./config
```

**Home Assistant won't start:**

```bash
docker-compose logs home-assistant
```

### Performance Optimization

- Add more CPU/memory allocation in docker-compose.yml if needed
- Use SSD storage for better performance
- Enable MariaDB or InfluxDB for better history management
- Consider using a reverse proxy for HTTPS

### Backing Up Configuration

```bash
# Backup your config directory
tar -czf home-assistant-backup.tar.gz config/

# Restore from backup
tar -xzf home-assistant-backup.tar.gz
```

### Additional Resources

- [Home Assistant Official Documentation](https://www.home-assistant.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Home Assistant Community](https://community.home-assistant.io/)
