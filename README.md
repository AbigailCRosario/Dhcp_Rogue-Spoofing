# Dhcp_Rogue-Spoofing
Rogue DHCP Server 

<p align="center">
  <img src="https://img.shields.io/badge/Attack-DHCP%20Spoofing-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Protocol-DHCP-blue?style=for-the-badge&logo=cisco" />
  <img src="https://img.shields.io/badge/Tool-Scapy-green?style=for-the-badge" />
</p>

> **⚠️ DISCLAIMER:** Este proyecto es una Prueba de Concepto (PoC) educativa. La ejecución de servidores DHCP falsos en redes reales puede causar pérdida total de conectividad y exposición de datos sensibles.  
> **Úsalo únicamente en laboratorios y entornos controlados.**

---

## 📖 Descripción del Escenario

El protocolo **DHCP** asigna dinámicamente direcciones IP a los clientes de la red.  
Este ataque explota la falta de autenticación del protocolo para **suplantar al servidor DHCP legítimo**.

El script `dhcp_rogue.py` responde más rápido que el gateway real y entrega a las víctimas:

- Gateway malicioso (atacante)
- DNS controlado por el atacante

**🎯 Objetivo:** Posicionar al atacante como **Gateway y DNS** de la red.  
**💥 Impacto:** *Man-in-the-Middle (MitM)*, redirección de tráfico, robo de credenciales y control del flujo de datos.

---

## 📺 Video Demostrativo

Mira el ataque en acción:

[![Ver Video del Ataque](https://img.shields.io/badge/YouTube-Ver%20Demo-red?style=for-the-badge&logo=youtube)](TU_ENLACE_AQUI)

---

## 🗺️ Topología de Laboratorio

El ataque se ejecuta desde un **puerto de acceso** simulando un **Insider Threat**.

| Dispositivo   | Rol Inicial     | Rol Final              | Interfaz | VLAN | Notas |
| :---          | :---            | :---                   | :---     | :--- | :--- |
| **R1-GTW**    | Gateway / DHCP  | Gateway legítimo       | `F0/0.11`| 11   | IP: 10.24.11.1 |
| **SW-ACCESO** | Switch Víctima  | Switch Víctima         | `Eth1/0` | 11   | Mode: Access |
| **Kali Linux**| Atacante        | **Gateway + DNS Fake** | `Eth0`   | 11   | IP: 10.24.11.10 |
| **Victim1**   | Cliente         | Cliente comprometido   | `Eth0`   | 11   | Recibe IP falsa |

---

## 📸 Paso a Paso: Ejecución del Ataque

### Paso 1: Estado Inicial

El cliente recibe su configuración IP del servidor DHCP legítimo (Gateway real).

![DHCP Legítimo](ruta/a/tu/imagen_dhcp_legitimo.png)

---

### Paso 2: Ejecución del Rogue DHCP

Ejecutamos el servidor DHCP falso desde Kali Linux.  
El script responde antes que el servidor real con un **DHCP OFFER malicioso**.

```bash
sudo python3 dhcp_rogue.py

¡Hecho! 👌 Te dejo estos últimos pasos del Rogue DHCP ya convertidos a Markdown listo para tu README.md de GitHub. Copia y pega tal cual donde corresponda en tu README:

### Paso 3: Confirmación del MitM

La víctima obtiene:

- **Gateway:** IP del atacante  
- **DNS:** IP del atacante  

👉 Todo el tráfico de la víctima ahora pasa por la **máquina atacante**.

---

## 🐍 Explicación del Script (`dhcp_rogue.py`)

El script utiliza **Scapy** para construir y enviar respuestas DHCP falsas en tiempo real:

- **Escucha `DHCP DISCOVER/REQUEST`:**  
  Intercepta solicitudes de clientes en broadcast.

- **Respuesta más rápida que el servidor real:**  
  Gana la “carrera” de ofertas DHCP.

- **Asignación de Gateway/DNS maliciosos:**  
  Redirige todo el tráfico de la víctima a través del atacante.

---

## 🛡️ Medidas de Mitigación

Para proteger la red contra **servidores DHCP falsos**, se deben aplicar las siguientes defensas en los **switches de acceso**:

---

### 1️⃣ DHCP Snooping (Trusted vs Untrusted)

Bloquea respuestas DHCP desde puertos no confiables (hosts de usuario).

```bash
SW-ACCESO(config)# ip dhcp snooping
SW-ACCESO(config)# ip dhcp snooping vlan 11

! Puerto de usuario (Untrusted)
SW-ACCESO(config)# interface Ethernet1/0
SW-ACCESO(config-if)# ip dhcp snooping limit rate 5

! Puerto uplink hacia el gateway legítimo (Trusted)
SW-ACCESO(config)# interface Ethernet0/2
SW-ACCESO(config-if)# ip dhcp snooping trust


### 2️⃣ Port Security 

Limita la cantidad de MACs por puerto, reduciendo la superficie de ataque.

```bash
SW-ACCESO(config)# interface Ethernet1/0
SW-ACCESO(config-if)# switchport port-security
SW-ACCESO(config-if)# switchport port-security maximum 3
SW-ACCESO(config-if)# switchport port-security violation restrict

