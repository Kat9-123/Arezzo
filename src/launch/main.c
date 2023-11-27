#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char FILE_NAME[] = "Arezzo.bat";

int main(int argc, char *argv[])
{

    int totalLength = strlen(FILE_NAME);


    for(int i=1; i<argc; i++)
    {
        // Spaces
        totalLength++;

        totalLength += strlen(argv[i]);
    }

    // Null terminated
    totalLength++;


    char command[totalLength];



    for(int i=0; i<strlen(FILE_NAME); i++)
    {
        command[i] = FILE_NAME[i];
    }

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
