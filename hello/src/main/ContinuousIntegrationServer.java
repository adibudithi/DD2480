package main;// compile & run: java -cp .:/home/nico/Documents/programming/ci_server/DD2480_CIserver/lib/json-20190722.jar:servlet-api-2.5.jar:jetty-all-$JETTY_VERSION.jar ContinuousIntegrationServer
// compile: javac -cp .:/home/nico/Documents/programming/ci_server/DD2480_CIserver/lib/json-20190722.jar:servlet-api-2.5.jar:/home/nico/Documents/programming/ci_server/DD2480_CIserver/lib/javax.mail-1.6.2.jar:/home/nico/Documents/programming/ci_server/DD2480_CIserver/lib/jakarta.activation-1.2.1.jar:jetty-all-$JETTY_VERSION.jar ContinuousIntegrationServer.java

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletException;

import org.json.*;

import javax.tools.DiagnosticCollector;
import javax.tools.JavaCompiler;
import javax.tools.ToolProvider;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.Request;
import org.eclipse.jetty.server.handler.AbstractHandler;


/**
 Skeleton of a main.ContinuousIntegrationServer which acts as webhook
 See the Jetty documentation for API documentation of those classes.
 */
public class ContinuousIntegrationServer extends AbstractHandler {

    public static String clone_url;
    public static String branch;
    public static String email;
    public static String sha;
    public static String buildpath = "/Users/adi/Downloads/builds";


    public void handle(String target,
                       Request baseRequest,
                       HttpServletRequest request,
                       HttpServletResponse response)
            throws IOException, ServletException
    {
        response.setContentType("text/html;charset=utf-8");
        response.setStatus(HttpServletResponse.SC_OK);
        baseRequest.setHandled(true);
        StringBuilder str = new StringBuilder();
        BufferedReader read = request.getReader();
        String line;
        if (request.toString().contains("POST")) {
            while ((line = read.readLine()) != null) {
                str.append(line);
            }
            String tmp_str;
            tmp_str = str.toString();
            System.out.println(tmp_str);
            jsonParser(tmp_str);
            getProjectFromGIT(clone_url, branch, buildpath);
            build(buildpath);
            System.out.println("build:" + str.toString());
            runtests();
            System.out.println("test:" + str.toString());

            String y = outputFromCI.toString();
            System.out.println(y);
            System.out.println(email);
            try {
                SendMail testy = new SendMail(email, y);
            }catch(Exception e) {
                e.printStackTrace();
            }
        }
        
        // here you do all the continuous integration tasks
        // for example
        // 1st clone your repository
        // 2nd compile the code

        //socket stuff
        System.out.println(baseRequest);
        System.out.println(baseRequest.toString());
        System.out.println(request.getReader());
        response.getWriter().println("CI job done");
    }


    ArrayList<File> javaFiles = new ArrayList<>();
    public StringBuilder outputFromCI = new StringBuilder();

    // used to start the CI server in command line
    public static void main(String[] args) throws Exception
    {
        Server server = new Server(8080);
        server.setHandler(new ContinuousIntegrationServer());
        server.start();
        server.join();   
    }

 /**
 *
 *Takes Source dir as string as input, this is then passed to listFilesForFolder() as a File.
 *When the listFilesForFolder() has populated the javaFiles<> it loops thorugh and compiles every file at its current location
 *
 */

    public void build(String souceDIR){

        File folder = new File(souceDIR);
        listFilesForFolder(folder);

        JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        DiagnosticCollector diagnosticsCollector = new DiagnosticCollector();

        String filesTOCompiles = "";
        for(File javaFile: javaFiles){

            filesTOCompiles = javaFile.getParent() + File.separator + javaFile.getName();
            System.out.println(filesTOCompiles = javaFile.getParent() + File.separator + javaFile.getName());

            OutputStream output = new OutputStream() {
                private StringBuilder string = new StringBuilder();

                @Override
                public void write(int b) throws IOException {
                    this.string.append((char) b );
                }

                //Netbeans IDE automatically overrides this toString()
                public String toString() {
                    return this.string.toString();
                }
            };

            int compileResult = compiler.run(null,null,output, filesTOCompiles);
            if(compileResult == 0){
                outputFromCI.append("Build successful \n");
                outputFromCI.append(output.toString());
            }else {
                outputFromCI.append("Build Failed \n");
                outputFromCI.append(output.toString());
                System.out.println(outputFromCI);

            }
        }
    }

 /**
 *Takes File as input and recursivly finds every .java file and adds them to javaFiles 
 */
    public void listFilesForFolder(File folder) {
        for (File fileEntry : folder.listFiles()) {
            if (fileEntry.isDirectory()) {
                listFilesForFolder(fileEntry);
            } else {
                if(fileEntry.getName().endsWith(".java")){
                    javaFiles.add(fileEntry);
                }
            }
        }
    }
    /**
    Run the tests in the repository. 
    All the files that contains "test" in their name is considered a test case and are run in this function.
    If the build fails the tests will not be ran. The function needs compiled files in the javaFiles array as input.
    The function appends the output from the test-files to outputFromCI, this includes the intended output from the test-files
    and if the there was an error during execution. The function returns everything the test-files returns.
    */
    public void runtests(){
        if(!(outputFromCI.toString().contains("Build Failed"))){
            for(File javaFile: javaFiles){
                if(javaFile.getName().toLowerCase().contains("test")){
                    String temp = javaFile.getName().replace(".java","");
                    String testFile = temp;
                    outputFromCI.append("================"+testFile+"===================\n");
                    try{
                        Process pro;
                        pro = Runtime.getRuntime().exec("java -cp "+javaFile.getParent()+" "+testFile);
                        //The stream obtains data piped from the standard output stream of the process
                        BufferedReader input = new BufferedReader(new InputStreamReader(pro.getInputStream()));
                        //The stream obtains data piped from the error output stream of the process
                        BufferedReader error = new BufferedReader(new InputStreamReader(pro.getErrorStream()));
                        String line1 = null;
                        String line2 = null;
                        //the output from the file
                        while ((line1 = input.readLine()) != null) {
                            outputFromCI.append(line1+"\n");
                        }
                        //the output if there is an error message
                        boolean err = true;
                        while ((line2 = error.readLine()) != null) {
                            if(err){
                              outputFromCI.append("Error in program: \n");
                              err = false;
                            }
                            outputFromCI.append(line2+"\n");
                        }
                        //wait until the process pro has terminated
                        pro.waitFor();
                        //exit value 0 is a successful termination
                        outputFromCI.append("exitValue() "+pro.exitValue());
                    } catch (Exception e){
                        System.out.println("error");
                    }
                }
            }
        }else{
            outputFromCI.append("Build failed, no tests were run");
        }
        String OS = System.getProperty("os.name").toLowerCase();
        try{
            if(OS.contains("win")){
                Process pro1 = Runtime.getRuntime().exec("cmd.exe /c start RD /S /Q "+javaFiles.get(0).getParent());
            }else {
                Process pro1 = Runtime.getRuntime().exec("rm -r  " + buildpath);
            }
        }catch (IOException ex){
            ex.printStackTrace();
        }
    }

 
 /**
 *Gets clone link and branch name from the webhook JSON and a static path is added when calling the function, then it will
 *start a commandline process and run the git clone commands. 
 */
 
    public void getProjectFromGIT(String cloneLink,String branchName, String storeAtPath) {

        String OS = System.getProperty("os.name").toLowerCase();

        if(OS.contains("win")){
            try {
                Runtime rt = Runtime.getRuntime();
                rt.exec("cmd.exe /c start git clone --branch "+ branchName + " " + cloneLink + " " + storeAtPath, null, new File(System.getProperty("user.home")));
                
              //Needs time to clone as it is a separate process so the code keeps running while the cloning is underwa
             System.out.println("Waiting 30 sek to clone");
                TimeUnit.SECONDS.sleep(30);

            } catch (Exception e){
                e.printStackTrace();
            }

        }else{
            try {
                Runtime rt = Runtime.getRuntime();
                rt.exec("git clone --branch "+ branchName + " " + cloneLink + " " + storeAtPath, null, new File(System.getProperty("user.home")));

                //Needs time to clone as it is a separate process so the code keeps running while the cloning is underway
                System.out.println("Waiting 30 sek to clone");
                TimeUnit.SECONDS.sleep(30);

            } catch (Exception e){
                e.printStackTrace();
            }
        }

    }
 
 /**
  * retrieves "clone_url", "branch", "email", and "sha" from a JSON-formatted string received from a GitHub webhook
  */
    public void jsonParser(String str){
        JSONObject obj = new JSONObject(str);
        clone_url = obj.getJSONObject("repository").getString("clone_url");
        String ref = obj.getString("ref");
        String[] refpath = ref.split("/");
        branch = refpath[refpath.length - 1];
        sha = obj.getString("after");
        email = obj.getJSONObject("pusher").getString("email");
    }

 /**
  * writes build history to a local file (buildHistory.txt) in JSON format
  */
    public void writeToFile(String filename) throws IOException {
        File f = new File(filename);
        if (!f.exists()) { // if first build
            PrintWriter writer = new PrintWriter(filename, "UTF-8"); // create file for writing
            JSONObject json = new JSONObject(); // create json

            JSONObject info = new JSONObject();
            info.put("clone_url", clone_url);
            info.put("branch", branch);
            json.put(sha, info);
            writer.print(json.toString()); // write json to file
            writer.close();
        } else if (f.exists() && !f.isDirectory()) { // if we have built before
            Path path = Paths.get(filename);
            String content = Files.readString(path); // read file
            PrintWriter writer = new PrintWriter(filename, "UTF-8"); // open file for writing
            JSONObject json = new JSONObject(content); // create json
            JSONObject info = new JSONObject();
            info.put("clone_url", clone_url);
            info.put("branch", branch);
            json.put(sha, info);
            writer.print(json.toString()); // write json to file
            writer.close();
        }
    }

}
