#include <iostream>
#include <string> 
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <sys/uio.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <netdb.h>
#include <unistd.h>
#include <vector>
#include <string>
#include <cstring>
#include <sstream>
#include <algorithm>
#include <fstream>

using namespace std;

int main(int argc, char * argv[]){
    // need IP address and port number of server

    if(argc != 3){
        cerr << " Please specify the IP address and port number" << endl;
        exit(0);
    }

    char *server_IP = argv[1];
    int port = atoi(argv[2]);
    struct hostent* host = gethostbyname(server_IP);
    sockaddr_in send_Stock_Address;

    //setting up the socket
    bzero((char*)&send_Stock_Address, sizeof(send_Stock_Address));
    send_Stock_Address.sin_family = AF_INET;
    send_Stock_Address.sin_port = htons(port);
    send_Stock_Address.sin_addr.s_addr = inet_addr(inet_ntoa(*(struct in_addr*)*host->h_addr_list));
    int clientSd = socket(AF_INET,SOCK_STREAM,0);
    //connnecting

    int status  = connect(clientSd, (sockaddr*)&send_Stock_Address, sizeof(send_Stock_Address));
    if(status < 0){
        cerr << "Error connecting to socket" << endl;
        exit(0);
    }

    cout<< "CONNECTION ESTABLISHED!!"<<endl;

    int count = 0;
    vector<string> buffer ( 1001, "");
    struct timeval start1, end1;
    gettimeofday(&start1, NULL);
    char msg[1000];
    char answer[1000000];
    while(true){
        cout<< "> ";
        int lineNum;
        string data;
        getline(cin,data);// take the command . neet to automatize this.
        memset(&msg,0,sizeof(msg));
        // logic figure.
        // of sending command 
        strcpy(msg, data.c_str());

        send(clientSd, (char*)&msg, strlen(msg),0);

        cout<< " SERVER IS RESPONDING ... " << endl;
        memset(&msg,0,sizeof(msg));
        memset(&answer,0,sizeof(answer));

        recv(clientSd, answer, sizeof(answer),0);
        cout<< " SERVER RESPONDED... " << endl;
        cout<< " SERVER SAYS: " << answer << endl;
    
        /*
        string response(answer);
        size_t firstLine = response.find("\n");
        if(firstLine != string::npos){
            string line1 = response.substr(0,firstLine);
            string line2  = response.substr(firstLine+1);
            cout<<line1<<endl;
            cout<<line2<<endl;
        }
        */

    }
    gettimeofday(&end1, NULL);
    close(clientSd);
    cout<< "CONNECTION CLOSED!!"<<endl;
    cout<< "Total time taken: " << (end1.tv_sec - start1.tv_sec) << " seconds" << endl;
    return 0;
}
