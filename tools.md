
---

### TOOLS.md

```markdown
# SlingShot IT Security Toolkit - Tool List

Below is a comprehensive list of tools available in the SlingShot IT Security Toolkit, organized by category. Each tool is accompanied by its icon (as displayed in the GUI) and a brief description.

## Security Tools
| Icon | Tool Name                  | Description                                              |
|------|----------------------------|----------------------------------------------------------|
| 🔑   | Generate Key              | Create encryption key.                                   |
| 🔐   | Encrypt File              | Secure file with key.                                    |
| 🔓   | Decrypt File              | Unlock encrypted file.                                   |
| 📊   | Hash File                 | Calculate file hash.                                     |
| 🗑️   | Shred File                | Securely delete file.                                    |
| 💪   | Password Manager          | Handle password tasks.                                   |
| 🔢   | OTP Generator             | Generate one-time codes.                                 |
| 🔒   | BitLocker Status          | Check encryption status.                                 |
| ✅   | Secure Boot Check         | Verify Secure Boot.                                      |
| 🛠️   | Harden Sys                | Enhance system security.                                 |
| 🛡️   | AV Status                 | Check antivirus status.                                  |
| 🦠   | Malware Scanner           | Detect malware.                                          |
| 🎣   | Phishing Detector         | Spot phishing attempts.                                  |
| 🔥   | Firewall Manager          | Control firewall settings.                               |
| 🔌   | USB Lockdown              | Block USB access.                                        |
| 🔒   | Password Policy Enforcer  | Set password rules.                                      |
| 📤   | Secure File Transfer      | Transfer files securely.                                 |
| 🔍   | Vuln Scan                 | Scan for vulnerabilities.                                |
| 📋   | Audit Policy Viewer       | View audit settings.                                     |
| 🕵️‍♂️ | Credential Harvester Detector | Detects attempts to harvest credentials via phishing or keylogging. |
| 🚫   | Rogue Process Terminator  | Terminates processes not matching a whitelist.           |
| 🗄️   | Secure File Vault         | Creates an encrypted vault for sensitive files.          |
| 🛡️   | Anti-Ransomware Shield    | Monitors and blocks ransomware-like file changes.        |
| 🔍   | Password Complexity Auditor | Audits stored passwords for complexity compliance.     |
| 🛠️   | Exploit Mitigation Checker | Verifies system exploit mitigation settings.           |
| 🎭   | Token Impersonation Detector | Detects processes using impersonated tokens.          |
| 🕳️   | Rootkit Scanner           | Scans for potential rootkit signatures.                  |
| ⏰   | Secure Deletion Scheduler | Schedules secure deletion of files.                      |
| 🔥   | Firewall Rule Analyzer    | Analyzes firewall rules for vulnerabilities.             |

## Monitoring Tools
| Icon | Tool Name                          | Description                                              |
|------|------------------------------------|----------------------------------------------------------|
| 📈   | Resource Monitor                  | Track system usage.                                      |
| 🖥️   | Service Monitor                   | Monitor services.                                        |
| 🔔   | Real-Time Alerts                  | Set system alerts.                                       |
| 🌡️   | CPU Temperature Monitor           | Track CPU temp.                                          |
| 📉   | Network Latency Graph             | Graph network latency.                                   |
| 📊   | Event Log Analyzer                | Analyze event logs.                                      |
| 💾   | Disk I/O Monitor                  | Monitor disk I/O.                                        |
| ⏳   | System Uptime Tracker             | Track uptime.                                            |
| ⏰   | Alert Scheduler                   | Schedule system alerts.                                  |
| 🚨🌐 | Network Connection Anomaly Detector | Spot network anomalies.                                |
| 📁🔍 | File System Anomaly Scanner       | Detect filesystem issues.                                |
| 🖥️📊 | Service Behavior Profiler         | Profile service behavior.                                |
| 📂🚨 | Registry Anomaly Detector         | Monitor registry changes.                                |
| 🕵️   | Network Intrusion Detection       | Detect network threats.                                  |
| 👤   | User Activity Logger              | Log user actions.                                        |
| 🌡️   | Process Heatmap                   | Visualize process activity.                              |
| 🌳   | Process Genealogy Tracker         | Tracks process parent-child relationships.               |
| 📡   | Network Traffic Anomaly Detector  | Detects anomalies in network traffic patterns.           |
| 🔗   | Service Dependency Monitor        | Monitors service dependencies for failures.              |
| ⏱️   | Disk Latency Monitor              | Tracks disk read/write latency.                          |
| 📊   | Memory Usage Profiler             | Profiles memory usage by process.                        |
| ⚖️   | CPU Core Load Balancer            | Monitors and reports CPU core load distribution.         |
| 🔗   | Event Log Correlation Analyzer    | Correlates event logs for suspicious patterns.           |
| 🌡️   | Thermal Stress Monitor            | Monitors system thermal stress levels.                   |
| 📶   | Network Connection Stability Tracker | Tracks network connection stability.                  |
| 🔮   | System Resource Forecasting       | Forecasts future resource usage trends.                  |

## Utility Tools
| Icon | Tool Name                  | Description                                              |
|------|----------------------------|----------------------------------------------------------|
| ℹ️   | System Info               | Show system details.                                     |
| 🧹   | Clear Temp Files          | Remove temp files.                                       |
| 👥   | List Users                | List system users.                                       |
| 💿   | Check Disk Health         | Assess disk condition.                                   |
| 🌍   | List Environment Vars     | Show env variables.                                      |
| 🔐   | File Permissions Viewer   | View file perms.                                         |
| 📂   | Registry Manager          | Edit system registry.                                    |
| 🔗   | Shortcut Creator          | Make app shortcuts.                                      |
| ♻️   | Recycle Bin Manager       | Handle recycle bin.                                      |
| ✔️   | File Integrity Checker    | Verify file integrity.                                   |
| 📝   | Text Encoder/Decoder      | Encode/decode text.                                      |
| 📸   | Screen Capture Tool       | Take screenshots.                                        |
| 📄   | PDF Merger                | Combine PDF files.                                       |
| 🔄   | Folder Sync               | Sync folder contents.                                    |
| 📂   | Duplicate File Finder     | Find duplicate files.                                    |
| 🖥️   | System Tray Manager       | Manage tray apps.                                        |
| 📋   | Clipboard Manager         | Handle clipboard history.                                |
| ✏️   | Batch File Renamer        | Rename files in bulk.                                    |
| 📋   | File Metadata Extractor   | Extracts metadata from files.                            |
| 🧹   | System Path Cleaner       | Cleans invalid entries from system PATH.                 |
| 📊   | File Extension Analyzer   | Analyzes file extensions in a directory.                 |
| 🔍   | Temporary File Scanner    | Scans and lists temporary files.                         |
| 📤   | Registry Key Exporter     | Exports a specified registry key.                        |
| 📝   | File Access Logger        | Logs file access attempts.                               |
| ⏰   | System Time Synchronizer  | Synchronizes system time with an NTP server.             |
| 💾   | Environment Variable Backup | Backs up environment variables.                        |
| 📦   | File Compression Tool     | Compresses files into a ZIP archive.                     |
| 💽   | Disk Space Analyzer       | Analyzes disk space usage.                               |

## Network Tools
| Icon | Tool Name                          | Description                                              |
|------|------------------------------------|----------------------------------------------------------|
| 🌐   | Network Monitor                   | Watch network activity.                                  |
| 🔎   | Port Scanner                      | Scan open ports.                                         |
| 📶   | Wi-Fi Analyzer                    | Analyze Wi-Fi networks.                                  |
| 🌐   | DNS Resolver                      | Resolve DNS names.                                       |
| 📡   | Packet Sniffer                    | Capture network packets.                                 |
| 📏   | Bandwidth Limiter                 | Limit app bandwidth.                                     |
| 📡👀 | Sniff Browser Activity            | Monitor browser login traffic.                           |
| 🌐⏳ | Dynamic DNS Resolver Monitor      | Monitor DNS changes.                                     |
| 📡🔍 | Network Packet Entropy Analyzer   | Analyze packet entropy.                                  |
| 📏   | Network Bandwidth Profiler        | Profiles network bandwidth usage.                        |
| 🌍   | IP Geolocation Tracker            | Tracks IP geolocation data.                              |
| 🕵️   | ARP Spoofing Detector             | Detects ARP spoofing attempts.                           |
| 🌐   | DNS Spoofing Detector             | Detects DNS spoofing attempts.                           |
| 🔎   | Network Device Scanner            | Scans for devices on the network.                        |
| 📡   | Packet Injection Detector         | Detects unusual packet injections.                       |
| 📶   | Wi-Fi Signal Strength Analyzer    | Analyzes Wi-Fi signal strength.                          |
| 📈   | Network Protocol Analyzer         | Analyzes network protocol distribution.                  |
| 🎭   | MAC Address Spoofer Detector      | Detects MAC address spoofing.                            |
| ⚡   | Network Latency Stress Tester     | Tests network latency under stress.                      |

## Backup Tools
| Icon | Tool Name                          | Description                                              |
|------|------------------------------------|----------------------------------------------------------|
| 💾   | Backup Manager                    | Manage backups.                                          |
| ✔️   | Backup Verifier                   | Check backup integrity.                                  |
| ⏰   | Backup Scheduler                  | Schedule backups.                                        |
| 🔄   | Differential Backup Tool          | Create differential backups.                             |
| 🔑   | Backup Encryption Key Manager     | Manage backup keys.                                      |
| ☁️   | Cloud Backup Uploader             | Upload to cloud.                                         |
| 📌   | Shadow Copy Manager               | Manage shadow copies.                                    |
| 🔄   | File Recovery Tool                | Recover deleted files.                                   |
| 🔙   | System Restore Point Creator      | Create restore points.                                   |
| ✔️   | Incremental Backup Verifier       | Verifies integrity of incremental backups.               |
| 📦   | Backup Compression Optimizer      | Optimizes backup compression ratios.                     |
| 📅   | Backup Schedule Auditor           | Audits scheduled backup executions.                      |
| 🗑️   | Backup Deduplication Tool         | Removes duplicates from backups.                         |
| 🔒   | Backup Encryption Auditor         | Audits encryption status of backups.                     |
| 🔄   | Backup Restore Simulator          | Simulates backup restoration.                            |
| 📑   | Backup Version Manager            | Manages multiple backup versions.                        |
| 📉   | Backup Space Optimizer            | Optimizes backup storage space.                          |
| 🔍   | Backup Integrity Scanner          | Scans backups for integrity issues.                      |
| 📊   | Backup File Hasher                | Generates hashes for backup files.                       |

## Advanced Tools
| Icon | Tool Name                          | Description                                              |
|------|------------------------------------|----------------------------------------------------------|
| ⚠️   | Process Manager                   | Manage active processes.                                 |
| 🕵️‍♂️ | Process Injection Detector        | Detect process injections.                               |
| 👻   | Process Hollowing Detector        | Detect hollowed processes.                               |
| 🕳️   | Memory Leak Detector              | Find memory leaks.                                       |
| 🧠   | Memory Forensics Lite             | Scan memory for clues.                                   |
| 🚨   | Kernel Driver Enumerator          | List kernel drivers.                                     |
| 🧵   | Thread Stack Analyzer             | Analyze thread issues.                                   |
| 🔝   | Privilege Escalation Checker      | Check privilege risks.                                   |
| ⌨️   | Keylogger Detector                | Find keyloggers.                                         |
| ❌   | Task Kill By Name                 | End task by name.                                        |
| 📞   | System Call Tracer                | Trace system calls.                                      |
| 🔐✅ | Secure Boot Policy Editor         | Edit Secure Boot.                                        |
| 🔄   | System Control                    | Control system state.                                    |
| 🧹   | DNS Cache Cleaner                 | Clear DNS cache.                                         |
| 🚗   | Driver Manager                    | Handle device drivers.                                   |
| 🥾   | Boot Manager                      | Adjust boot settings.                                    |
| 📤   | Sys Info Export                   | Export system info.                                      |
| 🖥️   | BIOS Info                         | Show BIOS details.                                       |
| 🖥️   | Remote Desktop Toggle             | Toggle remote access.                                    |
| ⚡   | Power Plan Manager                | Manage power plans.                                      |
| 📜   | Command History                   | View past commands.                                      |
| 📋   | Group Policy Viewer               | Show group policies.                                     |
| 🛠️   | Windows Feature Manager           | Control Windows features.                                |
| 🖥️   | Multi-Monitor Config              | Set up monitors.                                         |
| 🧹   | Event Log Cleaner                 | Clear event logs.                                        |
| 🚦   | Driver Verifier                   | Verify driver integrity.                                 |
| 🛠️   | System File Checker               | Fix system files.                                        |
| 🏁   | Performance Benchmark             | Test system performance.                                 |
| 🚀   | Startup Items                     | View startup programs.                                   |
| ⚡   | Startup Optimizer                 | Speed up startup.                                        |
| 💾   | Process Memory Dumper             | Dumps process memory to a file.                          |
| 🧠   | Kernel Memory Scanner             | Scans kernel memory for anomalies.                       |
| 📞   | System Call Interceptor           | Intercepts and logs system calls.                        |
| ✅   | Driver Signature Verifier         | Verifies signatures of loaded drivers.                   |
| 🕳️   | Memory Leak Injector              | Injects a memory leak for testing.                       |
| 🔝   | Process Privilege Auditor         | Audits process privileges.                               |
| ⚙️   | Thread Priority Adjuster          | Adjusts thread priorities.                               |
| ✔️   | System Integrity Verifier         | Verifies system file integrity.                          |
| 🚀   | Kernel Module Loader              | Loads a kernel module (simulated).                       |
| 📜   | Process Execution Tracer          | Traces process executions.                               |

## IT Support Tools
| Icon | Tool Name                          | Description                                              |
|------|------------------------------------|----------------------------------------------------------|
| 🖥️   | Remote Assistance Tool            | Start remote assistance.                                 |
| 👥   | User Account Manager              | Manage user accounts.                                    |
| 📈   | System Diagnostic Report          | Generate diagnostic report.                              |
| 🔗   | Service Dependency Viewer         | View service dependencies.                               |
| 🖥️   | Hardware Inventory Tool           | List hardware components.                                |
| ⏳   | Scheduled Task Manager            | Manage scheduled tasks.                                  |
| 📅   | Event Log Manager                 | Manage event logs.                                       |
| 👤   | User Session Manager              | Manages active user sessions.                            |
| 📥   | System Update Manager             | Manages system updates.                                  |
| 🖥️   | Remote Process Executor           | Executes a process on a remote machine.                  |
| 🔐   | User Permission Auditor           | Audits user permissions.                                 |
| 🔧   | Service Recovery Configurator     | Configures service recovery options.                     |
| 📜   | System Log Archiver               | Archives system logs.                                    |
| ⚠️   | Hardware Failure Predictor        | Predicts potential hardware failures.                    |
| 📋   | Group Policy Enforcer             | Enforces group policy settings.                          |
| 🖥️   | Remote Desktop Auditor            | Audits remote desktop connections.                       |
| 🤖   | Task Automation Script Generator  | Generates scripts for task automation.                   |

## Reconnaissance Tools
| Icon | Tool Name                          | Description                                              |
|------|------------------------------------|----------------------------------------------------------|
| 🌐🔍 | Sublist3r                         | Enumerate subdomains using Sublist3r.                    |
| 📜🔍 | crt.sh                            | Query crt.sh for subdomain certificates.                 |
| 🔎🌍 | Censys                            | Search Censys for subdomain data.                        |
| 📢   | Slack Notify                      | Send notifications to Slack.                             |
| 🌐   | Passive DNS Resolver              | Resolves domains passively via DNS records.              |
| 📋   | WHOIS Lookup Tool                 | Performs WHOIS lookups on domains.                       |
| 🔍   | Subdomain Enumerator              | Enumerates subdomains of a target domain.                |
| 🔒   | SSL Certificate Analyzer          | Analyzes SSL certificates of a domain.                   |
| 🗺️   | Network Topology Mapper           | Maps network topology.                                   |
| 🛤️   | Traceroute Analyzer               | Analyzes network traceroute data.                        |
| 👀   | DNS Cache Snooper                 | Snoops DNS cache for recent queries.                     |
| ⭐   | IP Reputation Checker             | Checks IP reputation scores.                             |
| 🚪   | Port Service Identifier           | Identifies services on open ports.                       |
| 📦   | Packet Header Analyzer            | Analyzes packet headers for insights.                    |

## Password Extraction Tools
| Icon | Tool Name                          | Description                                              |
|------|------------------------------------|----------------------------------------------------------|
| 🌐🔑 | Browser Password Extractor        | Extract browser passwords.                               |
| 🖥️🔑 | Windows Credential Manager Extractor | Pull system credentials.                              |
| 📋🔑 | Unified Password Aggregator       | Aggregate all passwords.                                 |

## Custom Tools
- **🛠️ Custom Tools**: Users can add their own Batch or PowerShell scripts via the "Manage Tools" interface, which are dynamically integrated into the appropriate category with the "🛠️" icon and a description like "Custom [script_type] script."

---

This list reflects all tools defined in the `FEATURE_ICONS` dictionary and categorized in the `get_categories()` method of the SlingShot toolkit as of the provided code snapshot.
