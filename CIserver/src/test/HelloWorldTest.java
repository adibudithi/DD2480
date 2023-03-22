public class HelloWorldTest{
  public static void main (String[] args){
    System.out.println("Hello World!");
    int i=1;
	int j=1;
    try{
	    if(i+j!=3){
	    	throw new Exception("1 + 1 = 2, it will never be 3");
	    }
	 
	}catch(Exception x){
		x.printStackTrace();
		System.out.println(x.getMessage());
	}
	 if(i+j==2){
	   System.out.println("Test successful");
	 }
  }
}
