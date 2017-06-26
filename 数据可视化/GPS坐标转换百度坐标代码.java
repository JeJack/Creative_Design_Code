import Ynu.Sei.cpLibrary.BASIC.cpIn;
import Ynu.Sei.cpLibrary.BASIC.cpOutput;
import org.apache.log4j.Logger;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import Ynu.Sei.cpLibrary.BASIC.cpIn;
import Ynu.Sei.cpLibrary.BASIC.cpOutput;
import Ynu.Sei.cpLibrary.cellgrid2D.Point2D;
import org.apache.log4j.Logger;

public class NewAppSendUtils {
    private static final Logger Log = Logger.getLogger(NewAppSendUtils.class);
    public static String connectURL(String dest_url, String commString) {
        String rec_string = "";
        URL url = null;
        HttpURLConnection urlconn = null;
        OutputStream out = null;
        BufferedReader rd = null;
        try {
            url = new URL(dest_url);
            urlconn = (HttpURLConnection) url.openConnection();
            urlconn.setReadTimeout(1000 * 30);
            //urlconn.setRequestProperty("content-type", "text/html;charset=UTF-8");
            urlconn.setRequestMethod("POST");
            urlconn.setDoInput(true);
            urlconn.setDoOutput(true);
            out = urlconn.getOutputStream();
            out.write(commString.getBytes("UTF-8"));
            out.flush();
            out.close();
            rd = new BufferedReader(new InputStreamReader(urlconn.getInputStream()));
            StringBuffer sb = new StringBuffer();
            int ch;
            while ((ch = rd.read()) > -1)
                sb.append((char) ch);
            rec_string = sb.toString();
        } catch (Exception e) {
            Log.error(e, e);
            return "";
        } finally {
            try {
                if (out != null) {
                    out.close();
                }
                if (urlconn != null) {
                    urlconn.disconnect();
                }
                if (rd != null) {
                    rd.close();
                }
            } catch (Exception e) {
                Log.error(e, e);
            }
        }
        return rec_string;
    }

    public static void main(String[] args) throws IOException {
        String fname="D:\\text1.txt";
        cpIn in= new cpIn(fname);
        String coords="";
        int i=0;
        FileReader fileReader=new FileReader(fname);
        BufferedReader br = new BufferedReader(fileReader);
        String str=null;
        while((str=br.readLine())!=null){
            i++;
            if(i%99==0){
                String result=connectURL("http://api.map.baidu.com/geoconv/v1/?coords="+coords+"&from=1&to=5&output=json&ak=LhZkh6wH9GG9kFZZ3cQDIEKji00IcnVp","");
                cpOutput out=new cpOutput("D:\\1result.txt");
            }
            System.out.println(str);
        }
        String result=connectURL("http://api.map.baidu.com/geoconv/v1/?coords="+coords+"&from=1&to=5&output=json&ak=LhZkh6wH9GG9kFZZ3cQDIEKji00IcnVp","");
        cpOutput out=new cpOutput("D:\\1result.txt");
        out.println(result);
        System.out.print(result);

    }
}
