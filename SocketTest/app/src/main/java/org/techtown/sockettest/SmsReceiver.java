package org.techtown.sockettest;

import android.app.Activity;
import android.app.Application;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.telephony.SmsMessage;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.RequiresApi;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Date;

public class SmsReceiver extends BroadcastReceiver {

    String contents = null;
    String from = null;

    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    public void onReceive(Context context, Intent intent) {
        // TODO: This method is called when the BroadcastReceiver is receiving
        // an Intent broadcast.
        Log.d("로그","onReceive() 메서드 호출됨.");

        Bundle bundle = intent.getExtras();
        SmsMessage[] messages = parseSmsMessage(bundle);


        if(messages != null && messages.length > 0){
            String sender = messages[0].getOriginatingAddress();
            Log.d("로그", "SMS sender: "+sender);

            contents = messages[0].getMessageBody().toString();
            from = sender;
            Log.d("로그", "SMS contents: "+ contents);

            Date receivedDate = new Date(messages[0].getTimestampMillis());
            Log.d("로그", "SMS received date: " + receivedDate.toString());
        }

        new Thread(new Runnable() {
            @Override
            public void run() {
                connectServer();
                //connectServer2();
            }
        }).start();




    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void connectServer()
    {
        // 소켓을 선언한다.
        try (Socket client = new Socket()) {
// 소켓에 접속하기 위한 접속 정보를 선언한다.
            InetSocketAddress ipep = new InetSocketAddress("192.168.43.5", 9999);
            //InetSocketAddress ipep = new InetSocketAddress("172.20.10.2", 80);
// 소켓 접속!
            client.connect(ipep);
// 소켓이 접속이 완료되면 inputstream과 outputstream을 받는다.
            try (OutputStream sender = client.getOutputStream();) {
                String msg = contents;;
// string을 byte배열 형식으로 변환한다.
                byte[] data = msg.getBytes();
// ByteBuffer를 통해 데이터 길이를 byte형식으로 변환한다.
                ByteBuffer b = ByteBuffer.allocate(4);
// byte포멧은 little 엔디언이다.
                b.order(ByteOrder.LITTLE_ENDIAN);
                b.putInt(data.length);
// 데이터 길이 전송
                sender.write(b.array(), 0, 4);
// 데이터 전송
                sender.write(data);
                data = new byte[4];



                InputStream receiver = client.getInputStream();
// 데이터 길이를 받는다.
                receiver.read(data, 0, 4);
// ByteBuffer를 통해 little 엔디언 형식으로 데이터 길이를 구한다.
                ByteBuffer bb = ByteBuffer.wrap(data);
                bb.order(ByteOrder.LITTLE_ENDIAN);
                int length = bb.getInt();
// 데이터를 받을 버퍼를 선언한다.
                data = new byte[length];
// 데이터를 받는다.
                receiver.read(data, 0, length);
// byte형식의 데이터를 string형식으로 변환한다.
                msg = new String(data, "UTF-8");

                ((MainActivity)MainActivity.mContext).alarm(from,msg);

            }
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    private SmsMessage[] parseSmsMessage(Bundle bundle) {
        Object[] objs = (Object[]) bundle.get("pdus");
        SmsMessage[] messages = new SmsMessage[objs.length];

        int smsCount = objs.length;
        for(int i=0;i<smsCount;i++)
        {
            if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M)
            {
                String format = bundle.getString("format");
                messages[i] = SmsMessage.createFromPdu((byte[]) objs[i], format);
            } else {
                messages[i] = SmsMessage.createFromPdu((byte[]) objs[i]);
            }
        }

        return messages;
    }



}
