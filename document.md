1. Socket Creation and Binding

    # USER SPACE
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_fd = server_socket.fileno()

    # KERNEL SPACE

        1. socket() System Call
            └── Kernel Entry
                ├── Allocate socket structure (struct socket)
                │   ├── Initialize protocol family (AF_INET)
                │   └── Setup TCP protocol operations
                ├── Create inode for socket
                │   └── Associate with VFS (Virtual File System)
                ├── Allocate file descriptor
                │   ├── Find lowest available FD number
                │   └── Create file structure
                └── Return FD to user space
    
        2. bind() System Call
            └── Kernel Entry
                ├── Lookup FD in process table
                ├── Validate address structure
                │   ├── Check address family
                │   └── Verify port availability
                ├── Create sock address structure
                │   ├── Convert IP address
                │   └── Network byte ordering
                ├── Update socket state
                │   ├── Set bound flag
                │   └── Associate address with socket
                └── Return to user space

2. Listen State Setup
    # USER SPACE
        server_socket.listen(5)  # Backlog of 5
    
    # Kernel Space Operations:
        1. listen() System Call
            └── Kernel Entry
                ├── Lookup socket from FD
                ├── Verify socket state
                │   └── Must be in CLOSED or BOUND state
                ├── Initialize listening state
                │   ├── Allocate accept queue
                │   │   ├── SYN queue (incomplete connections)
                │   │   │   └── Max size = backlog * 1.5
                │   │   └── Accept queue (completed connections)
                │   │       └── Max size = backlog
                │   └── Setup TCP listening state
                ├── Update socket operations
                │   ├── Change to passive mode
                │   └── Setup listening callbacks
                └── Return to user space

        Accept Queue Structure:
        +-------------------+
        | SYN Queue         |
        | (Half-open conns) |
        +-------------------+
                ↓
        +-------------------+
        | Accept Queue      |
        | (Established)     |
        +-------------------+

3. Accept Connection Process
    # USER SPACE
        client_socket, addr = server_socket.accept()
        client_fd = client_socket.fileno()
    
    # Kernel Space Operations:
        1. accept() System Call
            └── Kernel Entry
                ├── Lookup listening socket
                │   └── Verify LISTEN state
                │
                ├── Connection Establishment Process
                │   ├── SYN received from client
                │   │   └── Add to SYN queue
                │   ├── Send SYN-ACK
                │   ├── Receive ACK
                │   │   ├── Remove from SYN queue
                │   │   └── Move to accept queue
                │   └── Connection now ESTABLISHED
                │
                ├── New Socket Creation
                │   ├── Allocate new socket structure
                │   │   ├── Copy protocol info
                │   │   ├── Initialize TCP state
                │   │   └── Setup socket buffers
                │   │       ├── Receive buffer (default 87380 bytes)
                │   │       └── Send buffer (default 16384 bytes)
                │   ├── Allocate new file descriptor
                │   └── Setup socket operations
                │
                ├── TCP State Setup
                │   ├── Initialize sequence numbers
                │   ├── Setup TCP windows
                │   ├── Configure TCP options
                │   │   ├── Window scaling
                │   │   ├── SACK
                │   │   └── Timestamps
                │   └── Update routing info
                │
                ├── Memory Management
                │   ├── Allocate sk_buff structures
                │   ├── Setup DMA mappings
                │   └── Configure socket memory
                │
                └── Return to user space
                    ├── New client FD
                    └── Client address info

       
