# Next app

## Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

#### Opción 1: Compilar APK para instalación

```bash
# Compilar APK (debug, sin firmar)
flet build apk -v

# El APK se generará en: build/apk/app-release.apk
```

**Pasos para probar en Android:**

1. **Compilar el APK:**
   ```bash
   cd /home/israel/desarrollo/fletProjects/NextApp
   flet build apk -v
   ```

2. **Transferir el APK a tu dispositivo Android:**
   - Opción A: Conecta tu dispositivo por USB y copia el archivo `build/apk/app-release.apk`
   - Opción B: Envía el APK por email o servicios en la nube
   - Opción C: Usa `adb install` si tienes Android Debug Bridge instalado:
     ```bash
     adb install build/apk/app-release.apk
     ```

3. **Instalar en el dispositivo:**
   - Abre el archivo APK en tu Android
   - Permite la instalación desde fuentes desconocidas si es necesario
   - Instala la aplicación

4. **Ejecutar la app:**
   - Abre la app "Next App" desde el menú de aplicaciones
   - Prueba todas las funcionalidades para verificar la fluidez

#### Opción 2: Ejecutar directamente (desarrollo)

Si tienes un dispositivo conectado por USB con depuración USB habilitada:

```bash
# Ejecutar directamente en el dispositivo conectado
flet run -d android
```

**Requisitos previos para compilar:**
- Java JDK 11 o superior
- Android SDK (se descarga automáticamente en la primera compilación)
- Opcional: Android Studio para configuración avanzada

**Notas importantes:**
- La primera compilación puede tardar varios minutos (descarga dependencias)
- El APK generado será de debug (no firmado) - solo para pruebas
- Para distribución en Play Store, necesitarás firmar el APK

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).
