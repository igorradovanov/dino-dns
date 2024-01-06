# Dino DNS 🦕

This Python program implements DNS server using the UDP protocol based RFC 1035 standard. The server listens for incoming connections, receives data, processes it, and sends a response back to the client based on the Zones and the type of records defined (A, MX or TXT).

## Features

1. **DNS Query Processing**: The script processes DNS queries by extracting the domain name and question type from the query data.

2. **DNS Response Building**: The script builds a DNS response that includes the transaction ID, flags, question count, and answer count.

## Code Snippets

### DNS Query Processing

```python
for byte in data:
    if state == 1:
        domain_string += chr(byte)
        if x == expected_length:
            domain_parts.append(domain_string)
            domain_string = ''
            state = 0
        if byte == 0:
            domain_parts.append(domain_string)
            break
    else:
        state = 1
        expected_length = byte
x += 1
y += 1

question_type = data[y+1:y+3]

return (domain_parts, question_type)
```

This methods is responsible for processing the DNS query. It loops through the bytes in the data, converting them to characters and appending them to the domain string. When the end of a domain part is reached, it is added to the list of domain parts.

### DNS Response Building

```python
transaction_id = data[0:2]
TID = ''
for by in transaction_id:
    TID += hex(by)[2:]

flags = get_flags(data[2:4])

QDCOUNT = b'\x00\x01'

get_question_domain(data[12:])
```

This method is responsible for building the DNS response. It extracts the transaction ID, flags, and question count from the data, and gets the question domain.

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
