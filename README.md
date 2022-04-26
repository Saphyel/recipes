# Fantasy recipes

## Getting Started

### Prerequisites

Requirements:
* Docker-compose

Optional:
* Postman/Insomnia/curl
* Heroku CLI

### Start the project

Create `.env` file with:
```dotenv
DATABASE_URL=postgresql://postgres:password@db:5432/postgres
```

Inside the container execute:

```commandline
pdm install  # or pdm install --prod
```

For setting up the database run: `alembic upgrade head`


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
