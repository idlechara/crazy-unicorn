# Crazy Unicorn
An exploit for UtalcaAPP which allows users to attend any class as long as they are near any USB beacons.

## Motivation
* Contribute to QA process
* Satisfy my curiosity

## How does it works
Its decompiles the original APK and then injects a payload into it. The payload is used to track any communication between the cellphone to the servers and the beacons. The info tracked is used to grab auth credentials which allows to automate the process of getting an attendance mark on the platform.

## Pre-Requisites
* [GNU BASH](https://www.gnu.org/software/bash/)
* [Android Development Tools](https://developer.android.com/studio/index.html)
* [cURL](https://curl.haxx.se)
* [apktool](https://ibotpeaches.github.io/Apktool/)
* [keytool and jarsigner](https://stackoverflow.com/questions/4830253/where-is-the-keytool-application) (provided by Java SDK)
* [zipalign](https://stackoverflow.com/questions/31048208/zipalign-command-not-found) (provided by Android Development tools)
* [python2.7](https://www.python.org/download/releases/2.7/) (provided by Android Development tools)

## How to use it
```bash
chmod +x ./exploit.sh
./exploit.sh
```

## Security report (for academical purposes)
### Audit stage
I started by checking android log. This gave me some pointers about where to start digging.
![initial audit stage](images/initial_audit.png)
As it can be seen, the application was built using [ReactNative](https://facebook.github.io/react-native/) which is a JavaScript framework to build mobile applications. As every JS framework it suffers from the crux of low-skilled developers in terms of security and packaging.

### Dissasembly stage
After decompiling the apk I found some interesting things. 
* The beacon module is built as a native Java module, imported onto React.
* Most of the [smali](https://github.com/JesusFreke/smali) code looks like copypasted from another source or maybe two developers worked on this app.
* The features of the beacon module is to scan and bring up listeners to detect when a beacon is nearby.
* The beacon module is used on listeners of the ReactNative app, all variables are exposed to ReactNative as soon as a beacon shows up.
* Beacon detection is not triggered until the user gets the course list. Then, beacon detection turns on and continously scans for nearby beacons, changing flags for every course detected and enabling the "attend" button.
* Every query is made over **HTTP** [which is known by not being a safe protocol](https://www.entrepreneur.com/article/281633). This allows to track every comm between server and cellphone.
* Auth is made by sending credentials as plain text over HTTP, which can be easily intercepted.
* Every other method is secured by a session cookie installed onto the ReactNative webview. This cookie is not handled on any other place, which suggest that the developer doesn't know about token-based auth techniques.
* The following enpoints are hardcoded onto the application:


    * [POST] http://test.ingenieriautalca.cl/api/CuentaApi/Ingresar

        Body:
        ```javascript
        { 
            email: String, 
            password: String 
        }
        ```
        Returns: 
        ```javascript
        Number //The student id number
        ```

        This method also injects a session cookie, namely `.ASPXAUT`.

    * [POST] http://test.ingenieriautalca.cl/api/CursoApi/ProximasClases

        Body:
        ```javascript
        { 
            ID: String // The student id
        }
        ```
        Returns: 
        ```javascript
        //TODO
        ```

    * [POST] http://test.ingenieriautalca.cl/api/CursoApi/RegistrarAsistencia

        Body:
        ```javascript
        { 
            Clase: {
                ID: String // the course specific id for a given time.
            }, 
            Participante: {
                ID: String // the student id number
            }
        }
        ```
        Returns: 
        ```javascript
        //TODO
        ```
