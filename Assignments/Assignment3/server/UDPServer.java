// Source code is decompiled from a .class file using FernFlower decompiler.
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Hashtable;
import java.util.Random;

public class UDPServer {
   public static byte[] fileBytes;
   public static int numBytes;
   public static int numLines;
   Random random;
   Hashtable<String, ClientConn> ipAddresses;
   public static DatagramSocket datagramSocket;
   public static boolean variableRate;
   public static boolean tournament;
   public static boolean verbose;
   public static String md5Digest = "";
   public static int MAXLINES = 200;
   public static int MSS = 1448;

   public UDPServer() {
      numBytes = 0;
      numLines = 0;
      this.random = new Random();
      this.ipAddresses = new Hashtable();
      tournament = false;
      verbose = false;
   }

   public static void main(String[] var0) {
      UDPServer var1 = new UDPServer();
      if (var0.length < 4) {
         var1.log("Usage: java UDPServer [port number] [filename] [maxlines] [variablerate] [tournament] [verbose]");
      } else {
         int var2 = Integer.parseInt(var0[0]);
         String var3 = var0[1];
         MAXLINES = Integer.parseInt(var0[2]);
         String var4 = "";
         Random var5 = new Random(System.currentTimeMillis());
         variableRate = var0[3].equals("variablerate");
         tournament = var0[4].equals("tournament");
         verbose = var0[5].equals("verbose");
         fileBytes = new byte[MAXLINES / 10 * 3072];

         try {
            BufferedReader var6 = new BufferedReader(new FileReader(var3));
            FileWriter myWriter = new FileWriter("filename.txt");
            while(numLines < MAXLINES && (var4 = var6.readLine()) != null && var4.length() != 0) {
               if (var5.nextInt(10) > 3) {
                  initArray(fileBytes, numBytes, var4.getBytes());
                  numBytes += var4.length();
                  fileBytes[numBytes++] = 10;
                  ++numLines;
                  myWriter.write(var4);
               }
            }

            var1.log("Read lines: " + numLines);
            var1.log("Read bytes: " + numBytes);
            if (numLines < MAXLINES) {
               for(int var7 = numLines; var7 < MAXLINES; ++var7) {
                  var4 = "This is a padding line " + var7;
                  initArray(fileBytes, numBytes, var4.getBytes());
                  numBytes += var4.length();
                  fileBytes[numBytes++] = 10;
                  ++numLines;
               }
            }
         } catch (IOException var16) {
            var1.log("File exception: " + var16.getMessage());
            var16.printStackTrace();
            return;
         }

         byte[] var19;
         try {
            MessageDigest var17 = MessageDigest.getInstance("MD5");
            var17.update(fileBytes, 0, numBytes);
            var19 = var17.digest();
            StringBuilder var8 = new StringBuilder(var19.length * 2);
            byte[] var9 = var19;
            int var10 = var19.length;

            for(int var11 = 0; var11 < var10; ++var11) {
               byte var12 = var9[var11];
               var8.append(String.format("%02x", var12));
            }

            md5Digest = var8.toString();
            var1.log("MD5: " + md5Digest);
         } catch (NoSuchAlgorithmException var15) {
            var15.printStackTrace();
         }

         try {
            datagramSocket = new DatagramSocket(var2);
            var1.log("Server is listening on port " + var2);

            while(true) {
               var19 = new byte['\uffff'];

               try {
                  DatagramPacket var18 = new DatagramPacket(var19, var19.length);
                  datagramSocket.receive(var18);
                  var1.processPacket(var18, datagramSocket);
               } catch (Exception var13) {
                  var1.log("Read exception: " + var13.getMessage());
                  var13.printStackTrace();
               }
            }
         } catch (IOException var14) {
            var1.log("Server exception: " + var14.getMessage());
            var14.printStackTrace();
         }
      }
   }

   public static void initArray(byte[] var0, int var1, byte[] var2) {
      for(int var3 = 0; var3 < var2.length; ++var3) {
         var0[var1 + var3] = var2[var3];
      }

   }

   public static void initArray(byte[] var0, int var1, byte[] var2, int var3, int var4) {
      for(int var5 = 0; var5 < var4; ++var5) {
         var0[var1 + var5] = var2[var5 + var3];
      }

   }

   public void processPacket(DatagramPacket var1, DatagramSocket var2) {
      InetAddress var3 = var1.getAddress();
      String var4 = var1.getAddress().getHostAddress();
      int var5 = var1.getPort();
      byte[] var6 = var1.getData();
      long var8 = System.currentTimeMillis();
      ClientConn var7;
      if ((var7 = (ClientConn)this.ipAddresses.get(var4)) == null) {
         this.ipAddresses.put(var4, var7 = new ClientConn(var4, var8, this));
      }

      int var10 = 0;
      boolean var11 = true;
      boolean var12 = false;
      boolean var13 = false;
      boolean var14 = false;
      boolean var15 = false;
      String var16 = null;
      int var17 = -1;
      int var18 = -1;
      String var19 = "";
      String var20 = "";

      String var21;
      while(var11) {
         StringBuilder var22 = new StringBuilder();

         while(var6[var10] >= 32 && var6[var10] < 127 && var10 < var6.length) {
            var22.append((char)var6[var10++]);
         }

         if (var6[var10] == 10) {
            var16 = var22.toString();
            if (verbose) {
               this.log("Received: " + var4 + " - " + var16);
            }

            if (var16.startsWith("Offset")) {
               var17 = Integer.parseInt(var16.substring("Offset: ".length()));
               var13 = true;
            } else if (var16.startsWith("NumBytes")) {
               var18 = Integer.parseInt(var16.substring("NumBytes: ".length()));
               var13 = true;
            } else if (var16.startsWith("SendSize")) {
               var12 = true;
            } else if (var16.startsWith("Submit")) {
               var19 = var16.substring("Submit: ".length());
               var14 = true;
            } else if (var16.startsWith("MD5")) {
               var20 = var16.substring("MD5: ".length());
               var14 = true;
            } else if (var16.startsWith("Reset")) {
               var15 = true;
            } else if (var16.length() == 0) {
               var11 = false;
            }

            ++var10;
         } else {
            var21 = "ERROR: Invalid characters in header\n\n";
            this.sendPacket(var2, var3, var5, var21.getBytes(), 0, var21.length());
            if (verbose) {
               this.log("Sent ERROR: " + var4 + " - Invalid characters in header");
            }
         }
      }

      if (var12) {
         var21 = "Size: " + numBytes + "\n\n";
         this.sendPacket(var2, var3, var5, var21.getBytes(), 0, var21.length());
         if (verbose) {
            this.log("Sent size: " + var4 + ", size: " + numBytes);
         }
      }

      if (var13) {
         if (var17 >= 0 && var18 >= 0 && var18 <= MSS && var17 < numBytes) {
            if (var7.sendOrSkipData(var8)) {
               var6 = new byte['\uffff'];
               int var24 = Math.min(numBytes - var17 + 1, var18);
               String var23 = new String("Offset: " + var17 + "\nNumBytes: " + var24 + "\n");
               if (var7.isSquished()) {
                  var23 = var23 + "Squished\n\n";
               } else {
                  var23 = var23 + "\n";
               }

               initArray(var6, 0, var23.getBytes());
               initArray(var6, var23.length(), fileBytes, var17, var24);
               this.sendPacket(var2, var3, var5, var6, 0, var23.length() + var24);
               if (verbose) {
                  this.log("Sent data: " + var4 + ", offset: " + var17 + ", size: " + var24 + ", squished: " + var7.isSquished());
               }
            } else if (verbose) {
               this.log("Skipped request: " + var4 + ", offset: " + var17);
            }
         } else {
            var21 = "ERROR: Required header info not received\n\n";
            this.sendPacket(var2, var3, var5, var21.getBytes(), 0, var21.length());
            if (verbose) {
               this.log("Sent ERROR: " + var4 + " - Required header info not received");
            }
         }
      }

      if (var14) {
         if (!var19.equals("") && !var20.equals("")) {
            long var10000;
            if (var20.equals(md5Digest)) {
               var10000 = var8 - var7.getSessionStartTime();
               var21 = "Result: true\nTime: " + var10000 + "\nPenalty: " + var7.getCumulPenalty() + "\n\n";
               this.sendPacket(var2, var3, var5, var21.getBytes(), 0, var21.length());
               this.log("Sent success: " + var4 + ", time taken: " + (var8 - var7.getSessionStartTime()) + ", cumulPenalty: " + var7.getCumulPenalty() + ", runningPenalty: " + var7.getRunningPenalty());
            } else {
               var10000 = var8 - var7.getSessionStartTime();
               var21 = "Result: false\nTime: " + var10000 + "\nPenalty: " + var7.getCumulPenalty() + "\n\n";
               this.sendPacket(var2, var3, var5, var21.getBytes(), 0, var21.length());
               this.log("Sent failure: " + var4 + ", time taken: " + (var8 - var7.getSessionStartTime()) + ", cumulPenalty: " + var7.getCumulPenalty() + ", runningPenalty: " + var7.getRunningPenalty());
            }
         } else {
            var21 = "ERROR: Team name or MD5 not received\n\n";
            this.sendPacket(var2, var3, var5, var21.getBytes(), 0, var21.length());
            if (verbose) {
               this.log("Sent ERROR: " + var4 + " - Team name or MD5 not received");
            }
         }
      }

      if (var15 && !tournament) {
         var7.reset(var8);
      }

   }

   public synchronized void sendPacket(DatagramSocket var1, InetAddress var2, int var3, byte[] var4, int var5, int var6) {
      try {
         DatagramPacket var7 = new DatagramPacket(var4, var5, var6, var2, var3);
         var1.send(var7);
      } catch (Exception var8) {
         this.log("Send exception: " + var8.getMessage());
         var8.printStackTrace();
      }

   }

   public boolean loss(int var1) {
      return this.random.nextInt(100) <= var1;
   }

   public synchronized void log(String var1) {
      System.out.println(var1);
   }

   public synchronized void log(byte[] var1, int var2) {
      for(int var3 = 0; var3 < var2; ++var3) {
         System.out.print((char)var1[var3]);
      }

   }
}
