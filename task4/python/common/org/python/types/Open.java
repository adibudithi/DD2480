package org.python.types;
import java.lang.*;
import java.io.*;   //maybe import less

public class Open extends org.python.types.Object implements org.python.Object {
    private org.python.Object file;
    private org.python.Object mode;
    private org.python.Object buffering;
    private org.python.Object encoding;
    private org.python.Object errors;
    private org.python.Object newline;
    private org.python.Object closefd;
    private org.python.Object opener;
   
   //java.lang.Object
    public Open(org.python.Object file,
            org.python.Object mode,
            org.python.Object buffering,
            org.python.Object encoding,
            org.python.Object errors,
            org.python.Object newline,
            org.python.Object closefd,
            org.python.Object opener) {
            this.file=file;
            this.mode=mode;
            this.buffering=buffering;
            this.encoding=encoding;
            this.errors=errors;
            this.newline=newline;
            this.closefd=closefd;
            this.opener=opener;


            
            /*
            File toFile = new File(file.toString());
            FileReader fr = new FileReader(toFile);
            return fr;*/
       
    }

    public org.python.Object open2(){
        File toFile = new File(file.toString());
        FileReader fr = new FileReader(toFile);
        org.python.Object r = fr;
        return fr;
        
    }


}
