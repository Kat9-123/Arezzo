#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include<unistd.h>

const char FILE_NAME[] = "Arezzo.bat";

int main(int argc, char *argv[])
{
    /*We need to pass the given arguments to the bat file
    to do that we need to create a buffer with the correct size*/

    int bufferSize = strlen(FILE_NAME);

    // Loop through the args, the first arg is skipped because that is the path to the exe
    for(int i=1; i<argc; i++)
    {
        // Arguments are seperated by a single space
        bufferSize++;

        // Quotes will be added on both ends of the argument
        bufferSize += 2;

        bufferSize += strlen(argv[i]);
    }

    // Null terminated
    bufferSize++;


    char command[bufferSize];


    // Add the base command.
    for(int i=0; i<strlen(FILE_NAME); i++)
    {
        command[i] = FILE_NAME[i];
    }



    // Add the args
    int pos = strlen(FILE_NAME);

    for(int arg=1; arg<argc; arg++)
    {
        // A bit weird to do it like this, but it
        // is very clear what is happening
        command[pos] = ' ';
        pos++;
        command[pos] = '"';
        pos++;

        for(int c=0; c<strlen(argv[arg]); c++)
        {
            command[pos] = argv[arg][c];
            pos++;
        }
        command[pos] = '"';
        pos++;
    }


    command[pos] = '\0';

    chdir("Arezzo");
    system(command);
    return 0;
}
