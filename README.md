[![CodeQL](https://github.com/igorradovanov/dino-dns/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/igorradovanov/dino-dns/actions/workflows/github-code-scanning/codeql)

# Dino DNS 🦕

This Python program implements DNS server using the UDP protocol based RFC 1035 standard. The server listens for incoming connections, receives data, processes it, and sends a response back to the client based on the Zones and the type of records defined (A, MX or TXT).

## Features

1. **DNS Query Processing**: The script processes DNS queries by extracting the domain name and question type from the query data.

2. **DNS Response Building**: The script builds a DNS response that includes the transaction ID, flags, question count, and answer count.

## Docker Instructions

This application can be run using Docker. Here are the steps to do so:

1. **Build the Docker image**

You can build the Docker image using the following command:

```bash
docker build -t dino-dns .
```
This command builds a Docker image using the Dockerfile in the current directory and tags it as dino-dns.

2. **Run the Docker container**

After the image has been built, you can run the application in a Docker container with the following command:

```bash
docker run -p 53:53/udp dino-dns
```

This command runs the dino-dns Docker image as a container and maps the container's port 53 to the host's port 53.

Please note that you need to have Docker installed on your machine to execute these commands.

## Testing with `dig`

Once your DNS server is running, you can test it using the `dig` command. `dig` is a tool for querying DNS nameservers for information about host addresses, mail exchanges, nameservers, and related information.

Here's an example of how to use `dig` to test your DNS server:

```bash
dig @localhost -p 53 example.com
```

This command sends a DNS query to your server running on localhost at port 53 for the domain example.com. You should replace example.com with the domain you want to query.

Please note that dig is typically installed on most Unix-based systems by default. If you're on Windows, you can use nslookup for similar functionality.