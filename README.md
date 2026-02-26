# WAF-Pipeline

Problem Statement from SIH : 
Transformer based end-to-end Web Application Firewall (WAF) pipeline


Background
Traditional Web Application Firewalls (WAFs) rely primarily on static, rule-based detection (e.g., ModSecurity rules). These mechanisms struggle against zero-day exploits or never-seen-before attack patterns. Transformers, however, can learn complex request patterns from raw web traffic and detect anomalies without hard-coded signatures, offering a promising alternative. This challenge asks teams to build a complete pipeline from log ingestion → parsing → transformer-based training → real-time anomaly detection on a live web server.

Detailed Description
Participants will be provided with 3 (THREE) sample web application in war compressed format. They need to generate synthetic access log dataset representing benign requests only for the provided 03 applications. They shall use this data to further train the existing transformer models.

They must implement a complete system that supports:
Log Ingestion:
• Collect access logs from the web server (Apache or Nginx).
• Supports both batch ingestion (historical logs) and streaming ingestion (tailing live logs).
Parsing & Normalization:
• Extract key fields (method, path, parameters, headers, payload, etc.).
• Normalize/remove dynamic values (IDs, timestamps, tokens, etc.).
Tokenization & Input Transformation:
• Convert normalized requests into token sequences suitable for a Transformer-based model.
Model Training:
• Train an open-source Transformer-based model.
• Participants are free to select transformer architecture.
• Training can happen before the grand finale.
Real-Time Inference & Live Detection:
• Deploy the trained model alongside the sample app and integrate it with Apache or Nginx.
• The WAF component must receive each incoming request in real time and detect any anomalous request.
• Detections must run in non-blocking mode i.e multiple requests should be scanned simultaneously, without blocking each other or delaying normal traffic.
Continuous Updates:
• Provide an automated mechanism to re-train or fine-tune the existing model on new benign traffic.
• Update should be incremental, there should not be a need to retrain the model on full data, training will be done only on incremental data.
Demonstration:
• Use the supplied web application to show live detection of malicious requests.
• Participants will inject malicious payloads (e.g., via curl or script) to test detection.
• Judges will provide payload, requests to be done during grand finale to detect accuracy and detection ratio.

Expected Solution
Ingestion: Batch and real-time ingestion of access logs (commonly used format by apache/nginx).
Parser: Structured extraction, normalization.
Tokenizer: Prepares request sequence for Transformer.
Model Training: Transformer model trained on benign traffic.
Integration: Model integration into Apache/Nginx pipeline (via module, sidecar, or external micro service).
Non-Blocking Detection: Concurrent inference on real world traffic.
Continuous Update: Script / API for periodic retraining on incremental data only.
Demo: Live test of malicious input triggering detection log.
