package main; // source: https://javaee.github.io/javamail/
// source: https://github.com/eclipse-ee4j/jaf/releases
import javax.mail.*;
import javax.mail.internet.*;
import javax.naming.AuthenticationException;
import java.util.Properties;
import javax.activation.*;



/*
  Class used to send mail, method takes email address 
  and what the mail should output. Email is sent from send_from16@email.com
*/
//public class SendMail {
//
//  public SendMail (String email_address, String output) throws Exception {
//    // email address the mail is sent from
//    //String send_from = "send_from16@mail.com";
//    //String password = "password16";
//    // host and port for smtp server
//
//    String username = "nicolai.hellesnes@gmail.com";
//    String password = "MyPASSWORD";
//    String smtp_host = "smtp.gmail.com";
//    String smtp_port = "587";
//
//
//    // define the properties of the server
//    Properties properties = new Properties();
//    properties.put("mail.smtp.host", smtp_host);
//    properties.put("mail.smtp.port", smtp_port);
//    properties.put("mail.smtp.auth", "true");
//    properties.put("mail.smtp.socketFactory.port", smtp_port);
//    properties.put("mail.smtp.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
//
//    javax.mail.Authenticator auth = new javax.mail.Authenticator() {
//      protected PasswordAuthentication getPasswordAuthentication() {
//        return new PasswordAuthentication(username, password);
//      }
//    };
//
//    // create a new mail session
//    javax.mail.Session session = javax.mail.Session.getDefaultInstance(properties,auth);
//
//    // create a new email message object in the mime format
//    MimeMessage message = new MimeMessage(session);
//    message.setFrom(new InternetAddress(username));
//
//    // add all the recipients to the message
//    message.addRecipient(Message.RecipientType.TO, new InternetAddress(email_address));
//    message.setContent(message, "text/plain");
//    message.setSubject("CI notification");
//    message.setText(output);
//
//    // try to send email
//    try {
//      Transport.send(message);
//      System.out.println("Mail sent");
//    } catch (AuthenticationFailedException e) {
//      System.out.println("Something went wrong while trying to send the email");
//      throw new AuthenticationException();
//    }
//  }
//}

public class SendMail {

  public SendMail(String email_address, String output) {

    final String username = "adibudithi@gmail.com";
    final String password = "*********";

    Properties prop = new Properties();
    prop.put("mail.smtp.host", "smtp.gmail.com");
    prop.put("mail.smtp.port", "587");
    prop.put("mail.smtp.auth", "true");
    prop.put("mail.smtp.starttls.enable", "true"); //TLS

    Session session = Session.getInstance(prop,
            new javax.mail.Authenticator() {
              protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(username, password);
              }
            });

    try {

      Message message = new MimeMessage(session);
      message.setFrom(new InternetAddress("adibudithi@gmail.com"));
      message.setRecipients(
              Message.RecipientType.TO,
              InternetAddress.parse(email_address)
      );
      message.setSubject("CI Server Notification");
      message.setText(output);

      Transport.send(message);

      System.out.println("Done");

    } catch (MessagingException e) {
      e.printStackTrace();
    }
  }

}

// compile: javac -cp .:/home/nico/Documents/programming/ci_server/DD2480_CIserver/lib/jakarta.activation-1.2.1.jar:/home/nico/Documents/programming/ci_server/DD2480_CIserver/lib/javax.mail-1.6.2.jar SendMail.java
// compile & run: java -cp .:/home/nico/Documents/programming/ci_server/DD2480_CIserver/lib/jakarta.activation-1.2.1.jar:/home/nico/Documents/programming/ci_server/DD2480_CIserver/lib/javax.mail-1.6.2.jar SendMail.java
// info on how to get it to run: https://stackoverflow.com/questions/11459664/how-to-add-multiple-jar-files-in-classpath-in-linux

