# Lanzamiento: dominio, hosting, Supabase, AdSense y aspectos legales

Investigación realizada el 5 de octubre de 2026 para la web sobre las elecciones generales del 29 de noviembre de 2026.
No se ha comprado ni registrado nada. Los precios cambian a menudo, así que **comprueba siempre el precio final en el carrito antes de pagar**.

---

## Resumen rápido

| Decisión | Recomendación | Coste |
|---|---|---|
| Dominio | `elecciones-29n.es` (o `votar29n.es`), ambos parecen libres | ~7,25 € el primer año con IVA (OVHcloud) y ~8,46 € la renovación |
| Registrador | OVHcloud o DonDominio (precios honestos, sin una renovación que se dispare) | ver arriba |
| Hosting | Cloudflare Pages, plan gratuito (permite uso comercial y no tiene límite de ancho de banda) | 0 € |
| Backend del voto | Supabase Free, con el voto agregado y los resultados en caché | 0 €; opcionalmente Pro (25 $/mes) solo en noviembre |
| **Total del primer año** | | **≈ 7–8 €** (≈ 30 € si contratas Supabase Pro un mes) |
| Widget de voto | **Es legal recogerlo, pero sus resultados no pueden publicarse entre el 24 y el 29 de noviembre** (hasta que cierren las urnas). Además, durante el periodo electoral la JEC puede considerarlo una "encuesta", con todas sus obligaciones | — |

---

## 1. Disponibilidad de dominios

Método: consulta DNS (`nslookup -type=NS`) contra el DNS público de Google y consulta RDAP (rdap.org) para .com e .info. El registro .es (Red.es) no tiene un RDAP público, así que para los .es solo se ha podido comprobar el DNS.

| Dominio | Resultado | ¿Libre? | Confianza |
|---|---|---|---|
| elecciones29n.es | Tiene servidores de nombres `ns1/ns2.sedoparking.com` (aparcado en Sedo, probablemente **a la venta**) | **NO**, está registrado | Alta |
| elecciones29n.com | RDAP: **registrado hoy, 2026-10-05 07:18 UTC**, a través de **Cloudflare, Inc.**, con DNS de Cloudflare | **NO** | Muy alta. *Ojo: si lo has registrado tú hoy en Cloudflare, es tuyo. Si no, alguien se te ha adelantado esta misma mañana.* |
| elecciones29n.info | RDAP del registro: 404 "Object not found" | **Sí, libre** | Alta |
| elecciones-29n.es | NXDOMAIN (no existe en el DNS) | **Probablemente libre** | Media-alta (un .es podría estar registrado sin DNS, pero es raro) |
| generales29n.es | Aparcado en Sedo (`sedoparking.com`) | **NO**, registrado y probablemente a la venta | Alta |
| votar29n.es | NXDOMAIN | **Probablemente libre** | Media-alta |

**Recomendación:** `elecciones-29n.es`. Es el más parecido a la marca, se lee bien en voz alta como "elecciones guion 29 n punto es" y el .es da confianza al público español. La alternativa sin guion es `votar29n.es`. Antes de pagar, confírmalo en el buscador del registrador o en https://www.dominios.es (Red.es).

Si quieres `elecciones29n.es` o `generales29n.es`, puedes pujar en Sedo, pero suelen pedir cientos de euros. No compensa para una web de 2 meses.

---

## 2. Precios de dominios .es y .com (2026)

| Registrador | .es 1.er año | .es renovación | .com 1.er año / renovación | IVA | Fuente |
|---|---|---|---|---|---|
| **OVHcloud** | 5,99 € (**7,25 € con IVA**) | 6,99 € (**8,46 € con IVA**) | — | La página muestra ambos | https://www.ovhcloud.com/es-es/domains/tld/es/ |
| **DonDominio** | ~6,95 € | similar al registro (es su política) | — | Sin IVA | https://www.dondominio.com (dato de prensa: https://www.periodicodeibiza.es/noticias/economico/2021/05/07/1262479/dondominio-hace-facil.html, comprobar en la web) |
| **Hostinger** | 0,01 € | 9,99 €/año | — | No lo indica (suele ser sin IVA) | https://www.hostinger.com/es/dominio-es |
| **IONOS** | 1 € (promoción) / 10 € normal | 10 € | 1 € (promoción) / 15 € | Sin IVA | https://www.hosttest.es/comparativa/dominios.html (22/09/2026) |
| **Arsys** | 1 € (promoción) | 5 € según la tabla de Arsys / 25 € según comparativas: **confirmar** | 10 € / 25 € | Sin IVA | https://www.arsys.net/domains/prices |
| **Dinahosting** | ~11,13 $ (~9,75 €) | ~15,99 $ (~14 €) | — | Sin IVA | https://domainoffer.net/tld/es/dinahosting |
| **Strato** | 0,96 € (promoción) / 4,92 € | 4,92 € | — | Sin IVA | hosttest.es |
| **Cloudflare Registrar** | No vende .es | — | **.com 10,46 $** a precio de coste, igual en la renovación | Sin IVA | https://domainoffer.net/tld/com/cloudflare |
| **Porkbun** | **No vende .es** | — | ~11 $ | — | https://porkbun.com/tld/es |
| **Namecheap** | No se ha podido verificar (la web bloquea la consulta). Históricamente no vende .es | — | ~11 $ | — | — |

**Cuidado con las promociones a 1 € o 0,01 €.** La renovación luego sube. Por eso recomiendo OVHcloud (7,25 € el primer año y 8,46 € la renovación, ambos con IVA y anunciados claramente) o DonDominio.

**Requisitos del .es:** desde 2005 puede registrarlo cualquier persona física o jurídica con intereses o vínculos con España. Solo hace falta identificarse con **NIF/NIE** (o pasaporte si eres extranjero). Un particular español con DNI/NIF no tiene ningún problema. La norma la publica Red.es: https://www.dominios.es

---

## 3. Hosting para una web estática con anuncios

| Opción | ¿Uso comercial / AdSense? | Tráfico | Precio | Veredicto |
|---|---|---|---|---|
| **Cloudflare Pages (Free)** | **Sí, permitido** | **Ancho de banda y peticiones a archivos estáticos ilimitados**. 500 builds al mes, 20.000 archivos y 25 MiB por archivo | **0 €** | **RECOMENDADO** |
| Netlify Free | No está prohibido, pero… | 300 créditos al mes ≈ **30 GB de ancho de banda**. **Cuando se acaban los créditos, la web se PAUSA** ("Site not available") hasta el mes siguiente | 0 € | **Peligroso** en la noche electoral |
| Vercel Hobby | **PROHIBIDO.** Sus normas citan literalmente "The inclusion of advertisements, including … Google AdSense" como uso comercial, que requiere Pro (20 $/mes) | 100 GB | 0 € | **No sirve** |
| GitHub Pages | Prohíbe usarlo como hosting gratuito "to run your online business". Una web con AdSense está en zona gris | Límite blando de 100 GB al mes | 0 € | No recomendado |
| Hostinger compartido | Sí | Las tarifas no indican un límite de visitas (antes eran unas 10k–25k al mes). Un hosting compartido **se cae** con picos de cientos de miles de visitas | Single 1,49 €/mes, Premium 2,59 €/mes (con contrato de **48 meses**). Renovación: 6,99–9,99 €/mes. **Dominio gratis el primer año** en Premium o superior. IVA no indicado | Caro a largo plazo y peor ante picos |

Fuentes:
- Cloudflare Pages, límites: https://developers.cloudflare.com/pages/platform/limits/
- Cloudflare Workers, precios ("Requests to static assets are free and unlimited"): https://developers.cloudflare.com/workers/platform/pricing/
- Uso comercial en el plan gratuito de Cloudflare: https://developer.puter.com/blog/cloudflare-pages-alternatives/ y https://www.gigazine.net/gsc_news/en/20250116-why-cloudflare-pages-free
- Netlify, créditos y pausa: https://netli.fyi/blog/netlify-free-plan-limits-2026
- Vercel, uso comercial en Hobby: https://vercel.com/docs/limits/fair-use-guidelines (actualizado el 14/09/2026)
- GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- Hostinger: https://www.hostinger.com/es/hosting-web

**Montaje recomendado (0 €):**
1. Registrar `elecciones-29n.es` en OVHcloud o DonDominio.
2. Crear una cuenta gratuita en Cloudflare, añadir el dominio y cambiar los DNS del registrador a los de Cloudflare.
3. Publicar la carpeta `dist/` en Cloudflare Pages, subiéndola desde GitHub o directamente con `wrangler pages deploy dist`.
4. Usar el HTML y los JSON estáticos que sirve la CDN de Cloudflare. Así aguanta sin problema cientos de miles de visitas en la noche electoral, porque no hay un servidor que se pueda saturar.

El único punto débil ante un pico es el widget de voto contra Supabase (sección 4).

---

## 4. Supabase Free en 2026

Fuente: https://supabase.com/pricing

| | Free | Pro (25 $/mes) |
|---|---|---|
| Peticiones a la API | Ilimitadas | Ilimitadas |
| Base de datos | 500 MB | 8 GB |
| Egress (salida de datos) | **5 GB** (+5 GB en caché) | 250 GB (+250 GB en caché) |
| Servidor | CPU compartida, 500 MB de RAM (nano) | Micro, 1 GB de RAM (incluido) |
| Pausa por inactividad | **Se pausa tras 1 semana sin actividad** | Nunca |
| Edge Functions | 500.000 al mes | 2 millones al mes |
| Realtime | 200 conexiones simultáneas | 500 |
| Límite de gasto | — | Activado por defecto |

**¿Aguanta un voto viral?**
- **Guardar votos:** sí, si cada voto es un `INSERT` pequeño, o mejor aún un RPC que sume +1 a un contador por partido y provincia. 100.000 votos ocupan pocos MB.
- **El riesgo real son las lecturas de resultados.** Si 300.000 visitantes consultan los resultados cada pocos segundos (o con Realtime), se agotan los **5 GB de egress** y las **200 conexiones Realtime**, y el servidor nano se satura.
- **Solución gratuita:**
  - No usar Realtime.
  - Leer los resultados agregados una sola vez al cargar la página, o cada 60 s como mínimo.
  - Mejor todavía: poner delante un Worker de Cloudflare o una caché que sirva un JSON agregado con `Cache-Control: max-age=30–60`. El Worker gratuito permite 100.000 peticiones al día. Así Supabase solo recibe una petición por minuto.
  - Añadir protección antibots con Cloudflare Turnstile (gratis) y limitar las peticiones con RLS y RPC.
- **Pausa:** el proyecto gratuito se pausa si pasa 7 días sin actividad. Durante la campaña habrá tráfico, pero conviene programar un "ping" diario.
- **Cuándo pasar a Pro:** si se esperan más de 50.000–100.000 votantes reales en el widget o resultados casi en tiempo real. Basta con contratarlo **solo en noviembre** (unos 23 €) y bajar luego a Free.

---

## 5. Google AdSense en 2026 (web nueva en España)

**Requisitos** (https://support.google.com/adsense/answer/9724?hl=es):
- Tener **18 años o más**.
- Ser el **propietario** de la web y tener acceso al código HTML. Con tu dominio propio (`elecciones-29n.es`) se cumple. Un subdominio `*.pages.dev` no vale para solicitarlo.
- Contenido **original, de calidad y con suficiente texto**. Google no exige un mínimo de tráfico ni de antigüedad del dominio.
- Cumplir las políticas del programa y las políticas para editores.
- Tener una **política de privacidad** que mencione las cookies de Google y de terceros. En España, además, aviso legal (LSSI) y política de cookies.
- Tener un archivo **`ads.txt`** en la raíz (`/ads.txt`) con tu línea `google.com, pub-XXXX, DIRECT, f08c47fec0942fa0`.
- **CMP certificada (obligatoria en el EEE, Reino Unido y Suiza desde el 16/01/2024)** para mostrar anuncios a visitantes europeos. La opción más sencilla y **gratuita** es el CMP de Google, en *AdSense > Privacidad y mensajes > Mensaje del RGPD*. Fuente: https://support.google.com/adsense/answer/13554116?hl=es
- **Tiempo de aprobación:** "normalmente unos días, en algunos casos 2–4 semanas" (https://support.google.com/adsense/answer/9393996). **Como las elecciones son el 29/11, conviene solicitarlo esta misma semana**, con la web ya publicada y con contenido.
- **Rechazos típicos:**
  - "Contenido de poco valor": páginas casi vacías, solo datos sin texto propio, demasiadas páginas generadas automáticamente. Hay que añadir explicaciones y artículos originales.
  - "Sitio caído o no disponible": el dominio no resuelve, hay redirecciones, el robot de Google está bloqueado (robots.txt) o una pantalla de cookies o un muro tapa el contenido.
  - "Problemas de navegación": hace falta un menú claro y páginas "Quiénes somos" y "Contacto".
- **Contenido político:** está **permitido**. Las restricciones son para la desinformación, los contenidos manipulados ("misrepresentative content"), el odio, etc. Una web informativa y neutral sobre las elecciones es aceptable. Ten en cuenta que **desde octubre de 2025 Google no publica anuncios políticos en la UE** por el reglamento TTPA, así que no habrá anuncios de partidos. Además, algunos anunciantes evitan aparecer junto a contenido político, lo que **baja el RPM**. Fuentes: https://blog.google/company-news/inside-google/around-the-globe/google-europe/political-advertising-in-eu/ y https://ppc.land/google-updates-publisher-policies-to-forbid-political-misrepresentative-content
- **Umbral de pago:** **70 €** (https://support.google.com/adsense/answer/1709871). Pago mensual por transferencia, alrededor del día 21 del mes siguiente.
- **RPM orientativo para tráfico en español desde España:** Google paga sobre todo por impresión desde 2024. España rinde aproximadamente un 45 % del RPM de EE. UU. En noticias y política se puede esperar **entre 0,5 € y 2 € por cada 1.000 páginas vistas**. Ejemplo: 300.000 páginas vistas ≈ 150–600 €. Es una estimación aproximada. Fuentes: https://eastondev.com/blog/es/posts/media/20260108-google-adsense-guide/ y https://hacecuentas.com/calculadora-blog-adsense-rpm-nicho
- **Impuestos** (orientativo, **consulta con un gestor**):
  - Los ingresos de AdSense se declaran en el **IRPF**.
  - Google paga desde Google Ireland. Si la actividad es habitual, lo normal es darse de alta en Hacienda (modelo 036/037, epígrafe del IAE) y en el **ROI/VIES**, porque es una operación intracomunitaria: se factura sin IVA, con inversión del sujeto pasivo, y se presenta el **modelo 349**.
  - Si los ingresos son habituales, puede ser obligatorio darse de alta como **autónomo** (RETA, con tarifa plana para los nuevos autónomos). Para un ingreso puntual y pequeño se discute si basta con declararlo en el IRPF.
  - **Decídelo con un gestor antes de cobrar el primer pago.**

---

## 6. Aspectos legales: votación simbólica y LOREG

**Norma:** el art. 69.7 de la LOREG prohíbe "la publicación y difusión o reproducción de **sondeos electorales por cualquier medio de comunicación**" durante los **5 días anteriores a la votación**. Para el 29/11/2026, la prohibición va del **martes 24 al domingo 29 de noviembre, hasta el cierre de las urnas** (la JEC la extiende hasta el cierre, Acuerdo 184/1986). Además, el art. 69.1 obliga a que toda encuesta publicada **durante el periodo electoral** (desde la convocatoria) incluya una **ficha técnica**: entidad que la realiza y su domicilio, tamaño de la muestra, ámbito, texto completo de las preguntas y número de personas que no contestan.

**¿Está incluida una votación "simbólica" en una web?** La interpretación de la JEC es **muy amplia**:
- **Acuerdo JEC 93/2022 (26/05/2022):** es encuesta electoral "todo estudio que pretenda conocer el estado de opinión de todo o parte del electorado sobre su apoyo a las candidaturas".
- **Acuerdo JEC 608/2023 (03/08/2023):** la JEC rechaza el argumento de que fueran "estimaciones de usuarios". Lo que caracteriza a una encuesta es que refleja la intención de voto, "**con independencia de su denominación**". Fuente: [JEC, acuerdo 608/2023](https://www.juntaelectoralcentral.es/cs/Satellite?c=Page&childpagename=JEC%2FJEC_layout_HTML&cid=1379062426836&packedargs=esinstruccion%3Dfalse&materias=0&numExpediente=203&operadoracuerdo=-1&operadorobjeto=-1&template=Doctrina%2FJEC_DetalleHTML&tipoExpediente=300&tiposautor=0&pagename=jec%2Fwrapper%2FJEC_Wrapper)
- **Caso Electomanía (2022):** la JEC abrió un expediente sancionador por los "Emojipanel" (resultados disfrazados con comida y emojis) publicados en los 5 días anteriores a las elecciones de Castilla y León. Considera que esos disfraces son un **intento de eludir la prohibición**. Fuentes: https://www.eldebate.com/espana/20220401/jec-insiste-sancionar-difusion-sondeos-electorales-encubiertos-fuera-plazo-legal.html y https://www.que.es/2022/02/25/jec-expediente-electomania-sondeos-13f/
- La **Instrucción JEC 4/2007** aplica las normas electorales a internet y a las redes sociales (https://www.legalitas.com/actualidad/retuitear-hoy-un-sondeo-electoral-puede-ser-delito).
- **Sanciones:** multa de **3.000 a 30.000 €** (art. 153.2 LOREG). Por ejemplo, la JEC multó con 3.000 € al presidente del CIS en 2024, y el Tribunal Supremo lo confirmó. En casos graves puede haber además responsabilidad penal (art. 145 LOREG). Fuentes: https://blogs.uned.es/derechoyconstitucion/encuestas-electorales/ y https://www.poderjudicial.es/cgpj/es/Poder-Judicial/Tribunal-Supremo/Oficina-de-Comunicacion/Archivo-de-notas-de-prensa/El-Tribunal-Supremo-confirma-la-sancion-de-3-000-euros-de-la-Junta-Electoral-Central-al-presidente-del-CIS-por-no-comunicar-la--encuesta-flash-situacion-politica-espanola--realizada-en-abril-de-2024

No se ha encontrado ningún acuerdo de la JEC que excluya expresamente las votaciones "no científicas" o "simbólicas" de las webs. La doctrina apunta a lo contrario.

**Conclusión práctica:**
1. **Recoger votos está permitido.** La ley prohíbe *publicar* resultados, no preguntar.
2. **Del 24/11 a las 00:00 al 29/11 al cierre de las urnas** (20:00 en la península, 21:00 peninsular para incluir Canarias), **no mostrar resultados de ninguna forma**: ni porcentajes, ni gráficos, ni "quién va ganando", ni emojis, ni compartirlos en redes. Se puede dejar votar, pero los resultados se muestran después del cierre. Lo ideal es que se desactiven automáticamente por fecha **en el servidor**, no solo ocultándolos en el navegador.
3. **Desde la convocatoria hasta el 23/11**, publicar resultados de "intención de voto" puede exigir la ficha técnica del art. 69.1. Opción conservadora: mostrar los resultados con un aviso claro ("Votación simbólica sin valor estadístico, no es una encuesta ni un sondeo; muestra no representativa formada por los visitantes que han votado") **y** una ficha técnica mínima (responsable y domicilio, periodo, número de votos, pregunta literal). La opción más segura es **no publicar resultados por partido hasta el 29/11 a las 21:00** y, mientras tanto, mostrar solo "Gracias, tu voto se ha registrado (N votos)".
4. No uses trucos (frutas, emojis, colores) para insinuar resultados durante la prohibición.
5. Si hay dudas, se puede consultar a la Junta Electoral Central (consulta escrita, gratuita).

**RGPD (resumen):**
- Una votación sobre partidos es una **opinión política**, un dato de **categoría especial** (art. 9 RGPD) **si se puede vincular a una persona**.
- La **dirección IP es un dato personal** (sentencia del TJUE en el caso Breyer, C-582/14). Un hash de la IP sin más sigue siendo un dato *seudonimizado* y, por tanto, personal.
- **Recomendado:**
  - Guardar solo `partido + provincia + fecha`, sin IP, sin cookies de seguimiento y sin ningún identificador.
  - Para evitar votos dobles, usar una marca en el `localStorage` del navegador y Cloudflare Turnstile.
  - Si se necesita limitar por IP, hacerlo en memoria (límite de peticiones del Worker o de Cloudflare) sin guardarla. Otra opción es un hash con sal que **rota y se borra cada día**.
- Con datos realmente anónimos y agregados, el RGPD no se aplica a esos registros. Aun así, explícalo en la política de privacidad.
- Las cookies de AdSense sí requieren consentimiento, que gestiona la CMP de Google.

---

## Calendario sugerido

1. **Esta semana:** registrar el dominio, publicar en Cloudflare Pages, crear las páginas legales y `ads.txt`, y solicitar AdSense.
2. **Octubre:** aprobación de AdSense (de unos días a 4 semanas) y configuración del mensaje de RGPD en "Privacidad y mensajes".
3. **Del 24 al 29 de noviembre:** resultados de la votación ocultos desde el servidor.
4. **29 de noviembre a partir de las 21:00:** abrir los resultados de la votación y seguir el escrutinio. Es el momento de más tráfico.
5. **Diciembre:** volver a Supabase Free si se contrató Pro y vigilar los ingresos frente al umbral de pago de 70 €.
