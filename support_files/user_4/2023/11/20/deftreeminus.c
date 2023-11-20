
//libraries are imported here to use their functionalities
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include<stdbool.h>

#define MAX_LINE_SIZE 256

//this is the process to kill the parent of the defunct child
void terminateProcess(pid_t pid) {
    //SIGKILL is a signal to kill the process
    if (kill(pid, SIGKILL) == 0) {
        //Shwoing the message for the termination of process
        printf("Terminated process: %d\n", pid);
    } else {
        perror("kill");
    }
}

// this is the method to find the  defunct process in the given root 

// it has parameters like parent id, process id, whether the process which should not be deleted is given or not, and elapsed time

//it return void
void searchDefunctProcesses(const char *parentPID, int process_id) {

    // variable for the command which will be executed
    char command[MAX_LINE_SIZE];
    snprintf(command, sizeof(command), "ps -o pid,ppid,state --no-headers --ppid %s", parentPID);

    //execute the command
    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        perror("popen");
        return;
    }

    //get the details of each line
    char line[MAX_LINE_SIZE];
    while (fgets(line, sizeof(line), fp) != NULL) {
        // Parse the process information
        char pidStr[16];
        // pid will store the process id
        char ppidStr[16];
        //ppid will store the parent id
        char state[16];
    //state will store status of process

    //getting all the values
        sscanf(line, "%s %s %s", pidStr, ppidStr, state);
	
        // Check if the process is defunct
        if (strcmp(state, "Z") == 0) {
            pid_t pid = atoi(pidStr);
            int parent_id = atoi(ppidStr);
            
            if(parent_id != process_id){
                // Terminate the process and its parents
                    terminateProcess(parent_id);
            }
	
	}

        // Recursively search for defunct processes in the child process tree
        searchDefunctProcesses(pidStr, process_id);
    }

    pclose(fp);
}

//this is the main function
//this is where the execution begins
int main(int argc, char *argv[]) {
	bool isProcessGiven;
	int processNotBeDeleted;
    if (argc < 2) {
        printf("Usage: %s <process_id>\n", argv[0]);
        return 1;
    }

    if(argc > 2){
        // Checkes if excluded prcoess id is given or not
    	isProcessGiven=true;
    	if (argv[2][0] == '-') {
    	    processNotBeDeleted = atoi(argv[2]+1);
        }
        
    	printf("%d\n", processNotBeDeleted);
    }

    const char *rootPID = argv[1];
    searchDefunctProcesses(rootPID, processNotBeDeleted);

 return 0;
}
