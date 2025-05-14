/*
 * andrei-consumo.cpp
 *
 * Aplicación simple para medir el consumo energético estimado de un programa en Windows.
 * La herramienta lanza un proceso (pasado por argumentos) y, tras su finalización, utiliza
 * GetProcessTimes para obtener el tiempo de CPU (tiempo de proceso en modo usuario y kernel).
 *
 * Se estima el consumo energético multiplicando el tiempo total de CPU (en segundos)
 * por un factor de potencia (en vatios). En este ejemplo usamos 50W como valor aproximado.
 *
 * Compilar (ejemplo con Visual Studio):
 *     cl andrei-consumo.cpp
 *
 * Uso:
 *     andrei-consumo.exe <programa> [argumentos]
 *
 * Ejemplo:
 *     andrei-consumo.exe notepad.exe
 */

#include <windows.h>
#include <iostream>
#include <sstream>
#include <string>

/// Función auxiliar: Convierte un FILETIME (con intervalos de 100 ns) a un entero de 64 bits.
ULONGLONG fileTimeToULL(const FILETIME &ft) {
    ULARGE_INTEGER uli;
    uli.LowPart  = ft.dwLowDateTime;
    uli.HighPart = ft.dwHighDateTime;
    return uli.QuadPart;
}

/// Función para imprimir el error (si ocurre) basado en GetLastError.
void printLastError(const std::string &msg) {
    DWORD errCode = GetLastError();
    LPVOID lpMsgBuf;
    FormatMessageA(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
        nullptr,
        errCode,
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPSTR)&lpMsgBuf,
        0,
        nullptr
    );
    std::cerr << msg << " Error " << errCode << ": " << (char*)lpMsgBuf << std::endl;
    LocalFree(lpMsgBuf);
}

int main(int argc, char* argv[])
{
    if (argc < 2) {
        std::cout << "Uso: " << argv[0] << " <programa> [argumentos]" << std::endl;
        return 1;
    }

    // Concatenar los argumentos para formar la línea de comandos.
    std::ostringstream oss;
    for (int i = 1; i < argc; ++i) {
        // Si el argumento contiene espacios, lo ponemos entre comillas.
        std::string arg = argv[i];
        if (arg.find(' ') != std::string::npos) {
            oss << "\"" << arg << "\"";
        } else {
            oss << arg;
        }
        if (i < argc - 1) {
            oss << " ";
        }
    }
    std::string commandLineStr = oss.str();

    // En CreateProcess, el primer parámetro es el nombre del ejecutable. 
    // Aquí, extraemos el primer argumento como ruta del ejecutable.
    std::string appName = argv[1];

    // Preparamos la estructura STARTUPINFO y PROCESS_INFORMATION.
    STARTUPINFOA si;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    PROCESS_INFORMATION pi;
    ZeroMemory(&pi, sizeof(pi));

    // La función CreateProcess requiere que la cadena con la línea de comandos sea modificable.
    char* cmdLine = new char[commandLineStr.size() + 1];
    strcpy_s(cmdLine, commandLineStr.size() + 1, commandLineStr.c_str());

    // Crear el proceso a partir del comando.
    if (!CreateProcessA(
            appName.c_str(),   // aplicación a ejecutar
            cmdLine,           // línea de comandos (modificable)
            nullptr,           // atributos de proceso
            nullptr,           // atributos de hilo
            FALSE,             // heredar manejadores
            0,                 // flags de creación
            nullptr,           // variables de entorno
            nullptr,           // directorio actual
            &si,
            &pi
        ))
    {
        printLastError("Error al crear el proceso.");
        delete[] cmdLine;
        return 1;
    }
    delete[] cmdLine;

    std::cout << "Proceso lanzado: " << commandLineStr << std::endl;

    // Esperar a que el proceso finalice.
    WaitForSingleObject(pi.hProcess, INFINITE);

    // Obtener los tiempos de ejecución del proceso (usuario y kernel).
    FILETIME ftCreation, ftExit, ftKernel, ftUser;
    if (!GetProcessTimes(pi.hProcess, &ftCreation, &ftExit, &ftKernel, &ftUser)) {
        printLastError("Error al obtener los tiempos del proceso.");
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return 1;
    }

    // Convertir FILETIME a 64 bits y calcular el tiempo total en segundos.
    ULONGLONG kernelTime = fileTimeToULL(ftKernel);
    ULONGLONG userTime   = fileTimeToULL(ftUser);
    double totalTimeSeconds = (kernelTime + userTime) / 10000000.0; // 1 segundo = 10^7 intervalos de 100ns

    std::cout << "Tiempo total de CPU usado: " << totalTimeSeconds << " segundos" << std::endl;

    // Estimación del consumo energético.
    // Se asume que el consumo promedio del CPU durante la ejecución es de 50 vatios.
    const double potenciaEstimadaW = 50.0; // Valor estimado en vatios
    double energiaJoules = totalTimeSeconds * potenciaEstimadaW;
    
    std::cout << "Consumo energético estimado: " << energiaJoules << " Joules" << std::endl;

    // Cerrar los manejadores del proceso y del hilo.
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}