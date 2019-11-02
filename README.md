# Basic inventory APS

## Introduction

This is basic apis to administration inventory

## Installation 

The easiest install process, install first
[git](https://git-scm.com/downloads) and [docker](https://www.docker.com/get-started) in your system, latter continue with instructions.

Clone the repository:

```bash
$ git clone https://github.com/jgr7003/interview-brand-holding.git
```

Ingress to project directory and up the docker, wait while installing the container

```bash
$ cd interview-brand-holding/
$ docker-compose up
```

This will start the server on port 8006, and bind it to all network
interfaces. You can then visit the site at http://localhost:8006/ (Windows) or 
http://0.0.0.0:8006 (Mac)
- which will bring up swagger home page.

**Note:** The built-in CLI server is *for development only*.

## Administration

Ingress http://localhost:8006/admin the system will request user and password 

```
user: test
password: test
```

In this you can add products, stores, and initial inventories.

## APIs

To save the sale and discount the inventory, use the sales api http://0.0.0.0:8006/v1/api/sale/
and use the next body

```
{
	"number": "1",
	"store": "1",
	"details": [
		{
			"product_id": 1,
			"quantity": 1
		},
		{
			"product_id": 2,
			"quantity": 3
		}
	]
}
```

The another APIs you test in Swagger interface with not problem, some actions it´s restricted

## Transactional

The sale API is transactional whereby only save in the database if the process is successful.