# ⚙️ Proxies Puller

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**A high-performance, multi-threaded Python utility designed to automatically scrape, validate, deduplicate, and export working proxy servers.**

</div>

---

## 🚀 Overview

**Proxies Puller** is an advanced command-line tool built for developers, security researchers, and network analysts who require a reliable and fast supply of active proxies. It aggregates raw proxy lists from a wide variety of maintained open-source repositories and API endpoints, then verifies their live status in real-time using high-speed multi-threaded TCP socket connections.

---

## ✨ Key Features

* **Multi-Protocol Support**: Fetch and test proxies across **HTTP**, **SOCKS4**, and **SOCKS5** protocols.
* **Aggregated Sources**: Automatically pulls raw proxy lists from numerous reliable and frequently updated GitHub repositories and public APIs.
* **Concurrent Processing**: Utilizes Python's `concurrent.futures` for fast asynchronous source scraping and high-speed multi-threaded TCP socket validation.
* **Smart Deduplication**: Automatically filters out duplicate entries and merges results cleanly into your target text file.
* **Interactive CLI**: Clean, colored command-line interface featuring real-time scanning progress and live working statistics.

---

## 🛠️ Requirements & Dependencies

* **Python 3.x**
* **Requests Library**


## ⚠️ Disclaimer 
This tool is designed for educational purposes, ethical security research, and personal network testing. The author is not responsible for any misuse or illegal activities conducted using this software.
Always ensure you have permission or comply with the terms of service of the targets you interact with.
