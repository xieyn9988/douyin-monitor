# 抖音热点监控 Agent

> 一个基于 AI Coding 工具快速搭建的抖音数据采集与监控系统，用于公司内部音乐营销决策支持。

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.40%2B-green)
![SQLite](https://img.shields.io/badge/SQLite-3.0%2B-orange)
![Docker](https://img.shields.io/badge/Docker-24.0%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 目录

- [项目简介](#项目简介)
- [系统架构](#系统架构)
- [模块职责](#模块职责)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [测试验证](#测试验证)
- [数据库设计](#数据库设计)
- [核心实现细节](#核心实现细节)
- [Docker 部署](#docker-部署)
- [项目进展](#项目进展)
- [已知限制](#已知限制)
- [技术栈](#技术栈)
- [开发日志](#开发日志)
- [许可证](#许可证)
- [联系方式](#联系方式)

---

## 项目简介

本项目是一个**抖音热点监控 Agent**，旨在自动监控指定抖音账号的短视频内容，提取热点信息，进行结构化存储，为公司的音乐营销决策提供数据支持。

项目采用 **"AI 辅助开发 + 人工审核调试"** 的模式，在 **20 小时内**完成了从零到可运行原型的搭建，核心链路（采集 → 存储 → 日志）已全部打通。

### 核心价值

- **自动化采集**：无需人工手动翻看抖音，程序自动定时采集指定账号的最新视频
- **结构化存储**：将采集到的视频信息存入 SQLite 数据库，方便后续查询和分析
- **工程化保障**：具备日志记录、异常捕获、重试机制等生产级工程实践
- **容器化部署**：提供 Docker 支持，一键部署，环境一致

---

## 系统架构

```mermaid
graph TD
    A[调度器 Scheduler] -->|定时触发| B[采集模块 Collector]
    B -->|Playwright 浏览器自动化| C[抖音页面]
    C -->|提取视频信息| D[处理模块 Processor]
    D -->|FFmpeg 音频提取| E[存储模块 Storage]
    E -->|SQLite 数据库| F[(videos.db)]
    E -->|日志记录| G[日志模块 Logger]
    G -->|异常告警| H[告警模块 Alert]

    style A fill:#e1f5fe
    style B fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e9
    style G fill:#fce4ec
