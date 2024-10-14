#include <stdio.h>
#include <string.h>
#include <curl/curl.h>

int main() {
    CURL *curl;
    CURLcode res;
    char *url_base = "https://asciified.thelicato.io/api/v2/ascii?text=";
    char messages[] = "VENQMVB7ODNmZTAzNGIyY2ZiMDlkZWFmYmI5NTViMDMzOTJhMDgzZDhmODNiMn0K";
    char full_url[256];

    curl = curl_easy_init();
    if(curl) {
        while(1) {
            for (int i = 0; i < strlen(messages); i++) {
                snprintf(full_url, sizeof(full_url), "%s%c", url_base, messages[i]);
                
                curl_easy_setopt(curl, CURLOPT_URL, full_url);
                
                res = curl_easy_perform(curl);
            }
        }
        curl_easy_cleanup(curl);
    }
    return 0;
}
