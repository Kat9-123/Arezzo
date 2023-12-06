#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char FILE_NAME[] = "start \"Arezzo \" /d Arezzo Arezzo.bat";

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
        command[pos] = ' ';
        pos++;

        for(int c=0; c<strlen(argv[arg]); c++)
        {
            command[pos] = argv[arg][c];
            pos++;
        }
    }


    command[pos] = '\0';

    system(command);
    return 0;
}
