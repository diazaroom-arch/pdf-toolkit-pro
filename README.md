# 🚀 PDF Toolkit Pro

> Herramienta profesional de línea de comandos para automatización de PDFs

[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 ¿Qué es PDF Toolkit Pro?

PDF Toolkit Pro es una herramienta de línea de comandos potente y profesional diseñada para automatizar operaciones con archivos PDF a gran escala. Construida para desarrolladores, equipos de QA y empresas que necesitan procesar cientos o miles de PDFs de manera eficiente.

**Deja de perder tiempo con operaciones manuales de PDF.** Automatiza todo.

## ✨ Características

- ✅ **Combinar** múltiples PDFs en un solo documento
- ✅ **Dividir** PDFs por páginas, rangos o en páginas individuales
- ✅ **Extraer** páginas específicas de cualquier PDF
- ✅ **Información** detallada de archivos PDF
- ✅ **Contar páginas** rápidamente
- ✅ **Procesamiento por lotes** de directorios completos
- ✅ **Barras de progreso** para operaciones largas
- ✅ **Logging detallado** y manejo de errores
- ✅ **Multiplataforma** (Windows, macOS, Linux)

## 🚀 Inicio Rápido

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/diazaroom-arch/pdf-toolkit-pro.git
cd pdf-toolkit-pro

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar
pip install -e .
```

### Uso Básico
```bash
# Combinar PDFs
pdf-toolkit merge archivo1.pdf archivo2.pdf archivo3.pdf -o combinado.pdf

# Dividir PDF cada 10 páginas
pdf-toolkit split documento_grande.pdf --pages 10

# Contar páginas
pdf-toolkit count documento.pdf

# Información del PDF
pdf-toolkit info documento.pdf
```

## 📖 Documentación Detallada

### Operaciones de Combinación

#### Combinar múltiples archivos
```bash
pdf-toolkit merge reporte1.pdf reporte2.pdf reporte3.pdf -o reporte_final.pdf
```

#### Combinar todos los PDFs de un directorio
```bash
pdf-toolkit merge-dir /ruta/a/pdfs/ -o combinado.pdf
```

#### Combinar recursivamente (incluyendo subdirectorios)
```bash
pdf-toolkit merge-dir /documentos/ -o todos_los_docs.pdf --recursive
```

### Operaciones de División

#### Dividir cada N páginas
```bash
# Crear archivos de 10 páginas cada uno
pdf-toolkit split documento.pdf --pages 10
```

#### Dividir en páginas específicas
```bash
# Dividir en las páginas 25 y 50
pdf-toolkit split-at documento.pdf --at 25 --at 50

# Resultado: 3 archivos (páginas 1-24, 25-49, 50-final)
```

#### Dividir en páginas individuales
```bash
# Extraer cada página como PDF separado
pdf-toolkit split-pages documento.pdf --output-dir ./paginas/
```

#### Patrones de salida personalizados
```bash
pdf-toolkit split doc.pdf -p 5 --pattern "seccion_{num}.pdf"
# Crea: seccion_1.pdf, seccion_2.pdf, ...
```

### Información y Utilidades
```bash
# Obtener información detallada de un PDF
pdf-toolkit info documento.pdf

# Salida:
# 📄 Información del PDF: documento.pdf
#   Ruta:       /ruta/completa/al/documento.pdf
#   Tamaño:     2.5 MB
#   Páginas:    150
#   Metadatos:
#     Título:   Documento de Ejemplo
#     Autor:    Nombre del Autor

# Contar páginas rápidamente
pdf-toolkit count reporte.pdf
# 📄 reporte.pdf tiene 42 páginas

# Ver versión
pdf-toolkit version
```

## 🎯 Casos de Uso

### Para Desarrolladores
- Automatizar generación de reportes
- Procesar exportaciones PDF por lotes
- Crear datasets de prueba
- Construir pipelines de procesamiento de PDFs

### Para Equipos de QA
- Generar documentación de pruebas
- Combinar PDFs de resultados de tests
- Extraer casos de prueba específicos
- Organizar artefactos de testing

### Para Empresas
- Combinar lotes de facturas
- Dividir contratos grandes
- Organizar documentación
- Procesar envíos de formularios
- Gestión de archivos

## 🛠️ Detalles Técnicos

### Arquitectura
```
pdf-toolkit-pro/
├── src/pdf_toolkit/
│   ├── cli.py           # Interfaz de línea de comandos
│   ├── merge.py         # Operaciones de combinación
│   ├── split.py         # Operaciones de división
│   ├── utils.py         # Utilidades comunes
│   └── config.py        # Configuración
├── tests/               # Tests unitarios
└── examples/            # Ejemplos de uso
```

### Stack Tecnológico

- **Python 3.8+** - Características modernas de Python
- **pypdf** - Librería de manipulación de PDFs
- **Click** - Framework para CLI elegante
- **tqdm** - Barras de progreso
- **Pillow** - Procesamiento de imágenes
- **pytest** - Framework de testing

## 🧪 Testing
```bash
# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=pdf_toolkit

# Ejecutar archivo de test específico
pytest tests/test_merge.py
```

## 📦 Opciones Avanzadas

### Protección contra Sobrescritura

Por defecto, PDF Toolkit Pro no sobrescribirá archivos existentes:
```bash
# Esto fallará si output.pdf existe
pdf-toolkit merge *.pdf -o output.pdf

# Usar --overwrite para forzar
pdf-toolkit merge *.pdf -o output.pdf --overwrite
```

### Barras de Progreso
```bash
# Deshabilitar barra de progreso para scripts/automatización
pdf-toolkit merge *.pdf -o output.pdf --no-progress
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, siéntete libre de enviar un Pull Request.

1. Fork el repositorio
2. Crea tu rama de feature (`git checkout -b feature/CaracteristicaIncreible`)
3. Commit tus cambios (`git commit -m 'Agregar alguna CaracteristicaIncreible'`)
4. Push a la rama (`git push origin feature/CaracteristicaIncreible`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 💡 Autor

Creado por **diazaroom-arch**

- GitHub: [@diazaroom-arch](https://github.com/diazaroom-arch)

## 🙏 Agradecimientos

- Construido con [pypdf](https://github.com/py-pdf/pypdf)
- CLI con [Click](https://click.palletsprojects.com/)
- Inspirado por la necesidad de mejor automatización de PDFs

---

**⭐ Si encuentras útil este proyecto, por favor dale una estrella al repositorio!**

## 📊 Estadísticas

![GitHub stars](https://img.shields.io/github/stars/diazaroom-arch/pdf-toolkit-pro?style=social)
![GitHub forks](https://img.shields.io/github/forks/diazaroom-arch/pdf-toolkit-pro?style=social)

## 🔥 Ejemplos en Acción

### Procesamiento por Lotes
```bash
# Procesar 100 PDFs en segundos
for file in facturas/*.pdf; do
    pdf-toolkit split "$file" --pages 1
done
```

### Script de Automatización
```python
import os
from pdf_toolkit import merge_pdfs

# Combinar todos los reportes mensuales
reportes = [f"reporte_{i}.pdf" for i in range(1, 13)]
merge_pdfs(reportes, "reporte_anual.pdf")
```

---

**Hecho con ❤️ y Python**