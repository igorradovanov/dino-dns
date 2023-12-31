import socket

port = 53
ip = '127.0.0.1'

'''                                 1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    
    where:

ID              A 16 bit identifier assigned by the program that
                generates any kind of query.  This identifier is copied
                the corresponding reply and can be used by the requester
                to match up replies to outstanding queries.

QR              A one bit field that specifies whether this message is a
                query (0), or a response (1).

OPCODE          A four bit field that specifies kind of query in this
                message.  This value is set by the originator of a query
                and copied into the response.  The values are:

                0               a standard query (QUERY)

                1               an inverse query (IQUERY)

                2               a server status request (STATUS)

                3-15            reserved for future use

AA              Authoritative Answer - this bit is valid in responses,
                and specifies that the responding name server is an
                authority for the domain name in question section.

                Note that the contents of the answer section may have
                multiple owner names because of aliases.  The AA bit
                corresponds to the name which matches the query name, or
                the first owner name in the answer section.

TC              TrunCation - specifies that this message was truncated
                due to length greater than that permitted on the
                transmission channel.

RD              Recursion Desired - this bit may be set in a query and
                is copied into the response.  If RD is set, it directs
                the name server to pursue the query recursively.
                Recursive query support is optional.

RA              Recursion Available - this be is set or cleared in a
                response, and denotes whether recursive query support is
                available in the name server.

Z               Reserved for future use.  Must be zero in all queries
                and responses.

RCODE           Response code - this 4 bit field is set as part of
                responses.  The values have the following
                interpretation:

                0               No error condition

                1               Format error - The name server was
                                unable to interpret the query.

                2               Server failure - The name server was
                                unable to process this query due to a
                                problem with the name server.

                3               Name Error - Meaningful only for
                                responses from an authoritative name
                                server, this code signifies that the
                                domain name referenced in the query does
                                not exist.

                4               Not Implemented - The name server does
                                not support the requested kind of query.

                5               Refused - The name server refuses to
                                perform the specified operation for
                                policy reasons.  For example, a name
                                server may not wish to provide the
                                information to the particular requester,
                                or a name server may not wish to perform
                                a particular operation (e.g., zone


                                transfer) for particular data.

                6-15            Reserved for future use.

QDCOUNT         an unsigned 16 bit integer specifying the number of
                entries in the question section.

ANCOUNT         an unsigned 16 bit integer specifying the number of
                resource records in the answer section.

NSCOUNT         an unsigned 16 bit integer specifying the number of name
                server resource records in the authority records
                section.

ARCOUNT         an unsigned 16 bit integer specifying the number of
                resource records in the additional records section.
'''

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))

def get_flags(flags):
    
    byte1 = bytes(flags[0:1])
    byte2 = bytes(flags[1:2])
    
    rflags = ''
    
    # Get QR Flag
    QR = 1
    
    # Get OPCODE
    OPCODE = ''
    
    for bit in range(1,5):
        OPCODE += str(ord(byte1)&(1<<bit))
        
    # Get AA Flag
    
    AA = '1'
    
    # Get TC Flag
    
    TC = '0'
    
    # Get RD Flag
    
    RD = '0'
    
    # Get RA Flag
    
    RA = '0'
    
    # Get Z Flag
    
    Z = '000'
    
    # Get RCODE Flag
    
    RCODE = '0000'
    
    return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(2, byteorder='big')+int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')

def get_question_domain(data):
    
    state = 0
    expected_length = 0
    domain_string = ''
    domain_parts = []
    x = 0
    y = 0
    
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

def build_response(data):
    
    # Transcation ID
    transaction_id = data[0:2]
    TID = ''
    for by in transaction_id:
        TID += hex(by)[2:]
    
    # Get the Flags
    flags = get_flags(data[2:4])
    
    # Question Count
    QDCOUNT = b'\x00\x01'
    
    # Answer Count
    get_question_domain(data[12:])

while True: # listen for connections
    data, addr = s.recvfrom(1024)
    print(data)
    r = build_response(data)
    s.sendTo(r, addr) # returns a response to the client in bytes
    