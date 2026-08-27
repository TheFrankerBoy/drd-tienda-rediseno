# Rediseño Tienda DRD — propuesta

Propuesta de rediseño de la tienda online de **DRD SLL** ([tienda.drdsll.com](https://tienda.drdsll.com/)).

**En vivo:** https://thefrankerboy.github.io/drd-tienda-rediseno/

> **Esto es una DEMO.** No es el sitio oficial de DRD SLL ni está asociada a la empresa.
> Las fotos de producto y los precios proceden del catálogo público de DRD SLL y de sus
> fabricantes, y se usan únicamente para ilustrar esta propuesta. El stock, los plazos y
> las medidas son datos de ejemplo.

## Qué incluye

- Buscador por **referencia**, medida, marca o nombre, con navegación por teclado.
- **Pedido rápido por lista de referencias**: pegas el albarán y sale el pedido.
- **Cajón de pedido** con cantidades, base imponible, IVA y **portes calculados en vivo**.
- Interruptor **precio sin IVA / con IVA** en toda la página.
- **Ficha rápida** con datos técnicos, stock y descuento.
- Filtros por familia, orden por precio o stock y «sólo con stock».
- Descarga del **presupuesto en CSV**.
- **Calculadora de portes** por destino con umbral de envío gratis.
- Responsive, menú móvil y barra de progreso de lectura.
- Tabla *«Qué arregla este rediseño»*: los 9 problemas detectados en el sitio actual, cada
  uno con su solución.

## Sobre las fotos

Las fotos del catálogo actual llevan el rótulo «OUTLET» **quemado dentro del JPG**, incluso
en el archivo original. Se han descargado y limpiado por detección de componentes conexas
(`tools/dewatermark.py`) para que el «Outlet» pase a ser una etiqueta del sistema:
filtrable, ordenable y que desaparece sola cuando termina la oferta.

## Técnica

Una sola página HTML autocontenida (`index.html`): CSS y JS en línea, sin dependencias
más allá de Google Fonts (Archivo + IBM Plex Sans/Mono). La paleta está tomada del tema
real de la tienda (`theme-ff5c00.css`): naranja `#FF5C00` sobre blanco.
