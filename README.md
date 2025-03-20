📌 Sistema de Monitoramento e Análise Preditiva para Manutenção Industrial

🔍 Objetivo

Desenvolver um sistema avançado de detecção de anomalias em maquinários industriais, utilizando Machine Learning e sensores IoT. O sistema será capaz de identificar e prever falhas operacionais com base na análise contínua de dados de temperatura, vibração, umidade e consumo de energia, permitindo a implementação de estratégias de manutenção preditiva para otimização do desempenho industrial.

⚠️ Problema a Ser Resolvido

Atualmente, a manutenção de máquinas industriais enfrenta desafios como:
	•	Falhas inesperadas 🛑 — Paradas não planejadas impactam a produtividade e aumentam custos operacionais.
	•	Alto custo de manutenção corretiva 💰 — Reparos emergenciais exigem maior investimento e reduzem a vida útil dos equipamentos.
	•	Dificuldade na identificação de padrões de anomalia 🔍 — Sensores coletam grandes volumes de dados, mas a análise manual é lenta e imprecisa.
	•	Falta de previsibilidade 📉 — Empresas não conseguem antecipar falhas antes que impactem a operação.

🏆 Solução Proposta

Nosso sistema proporciona uma abordagem baseada em inteligência artificial e análise estatística, permitindo:

✅ Monitoramento contínuo dos equipamentos em tempo real.
✅ Detecção automática de anomalias utilizando o modelo Mahalanobis.
✅ Predição de falhas com base em padrões históricos.
✅ Redução de custos operacionais ao permitir manutenções planejadas.
✅ Integração flexível com sistemas IoT para aquisição e processamento de dados.

🚀 Tecnologias Utilizadas
	•	🖥️ Backend: FastAPI para a API de análise preditiva.
	•	📊 Machine Learning: Algoritmo de distância de Mahalanobis para detecção de anomalias.
	•	🛠️ Infraestrutura: Docker para containerização e implantação eficiente.
	•	📡 Sensores IoT: Coleta de dados de temperatura, vibração e consumo de energia.

---

## 🎯 Principais Componentes

- **Sensores IoT**: Dispositivos de monitoramento para aquisição de variáveis ambientais e operacionais, incluindo sensores de temperatura, vibração, umidade e consumo energético.
- **Plataforma de Coleta de Dados**: Middleware responsável pela captura, armazenamento e processamento dos dados provenientes dos sensores IoT.
- **Machine Learning**: Modelos de aprendizado de máquina treinados para identificar padrões anômalos e prever falhas futuras.
- **Interface Web/Dashboard**: Plataforma de visualização interativa para monitoramento em tempo real, alertas de anomalias e geração de relatórios analíticos.

---

## 🔬 Estratégia de Coleta e Treinamento de Dados
1. **Fase Inicial - Coleta de Dados Normais**
   - Registrar dados operacionais de equipamentos em **condições normais de funcionamento**.
   - Determinar padrões estatísticos para definir um estado de referência.

2. **Simulação de Anomalias**
   - Induzir e registrar comportamentos anômalos nos equipamentos.
   - Capturar dados de erro para compor um dataset robusto e representativo.

3. **Treinamento do Modelo de Machine Learning**
   - Utilizar os dados coletados para treinar algoritmos supervisionados e não supervisionados.
   - Implementar técnicas como **Random Forest, SVM, LSTMs e Autoencoders** para aprimorar a detecção de falhas.

---

## ⚡ Primeiros Testes e Infraestrutura
- Utilização de um **acelerômetro de 3 eixos** para análise de vibração mecânica.
- Conectividade inicial via **ESP8266** utilizando **Wi-Fi** para transmissão de dados.
- Implementação de um pipeline de dados para análise em tempo real.
- Após validação do modelo, avaliação de protocolos de comunicação alternativos, incluindo **BLE, Zigbee e LoRaWAN**, para maior flexibilidade e escalabilidade da solução.

## 📌 Etapas do Projeto

### 1️⃣ Replicar Sensores
- Escolher sensores IoT para coleta de temperatura, vibração e umidade.
- Integrar sensores com microcontroladores (ESP32, Raspberry Pi, Arduino).
- Estabelecer comunicação via MQTT, LoRaWAN ou outro protocolo adequado.

### 2️⃣ Coletar Dados
- Definir frequência e formato de coleta.
- Armazenar dados em um banco de dados adequado (InfluxDB, PostgreSQL, MongoDB).
- Criar API para comunicação entre sensores e banco de dados.

### 3️⃣ Tratar Dados
- Limpar e organizar os dados coletados.
- Normalizar e padronizar valores para melhorar a qualidade do modelo.
- Aplicar filtros para remoção de ruídos (média móvel, FFT para vibração).

### 4️⃣ Extrair Features
- Identificar padrões e variáveis relevantes.
- Criar novas variáveis derivadas para aprimorar a análise.
- Utilizar algoritmos de seleção de features (PCA, ANOVA, correlação).

### 5️⃣ Treinar Modelo
- Escolher o algoritmo mais adequado (Random Forest, SVM, Redes Neurais, LSTMs).
- Treinar modelos com os dados tratados.
- Testar diferentes abordagens para otimização de desempenho.

### 6️⃣ Validar
- Testar modelo com novos dados.
- Ajustar hiperparâmetros para melhorar a precisão.
- Implementar modelo na plataforma de monitoramento.

---

## 🛠 Tecnologias Utilizadas
- **Sensores**: MPU6050 (vibração), DHT22 (umidade), MLX90614 (temperatura), ACS712 (corrente elétrica).
- **Microcontroladores**: ESP32, Raspberry Pi.
- **Protocolo de Comunicação**: MQTT, LoRaWAN.
- **Banco de Dados**: InfluxDB (time series), PostgreSQL/MongoDB.
- **Linguagens**: Python (para ML e processamento de dados), C++/MicroPython (para IoT).
- **Bibliotecas de Machine Learning**: Scikit-learn, TensorFlow, PyCaret.
- **Framework para Dashboard**: Streamlit, Grafana, Flask/Django.

---

## 📢 Como Contribuir
Se você deseja contribuir com o projeto:
1. Faça um **fork** do repositório.
2. Crie uma **branch** com a sua feature (`git checkout -b minha-feature`).
3. Faça o **commit** das suas alterações (`git commit -m 'Adicionando nova feature'`).
4. Faça o **push** para a sua branch (`git push origin minha-feature`).
5. Abra um **Pull Request**.

---

Referencias:
https://tractian.com/sensor-de-vibracao-para-zonas-ex?utm_source=google&utm_medium=cpc&utm_campaign=bra-conversion-institutional-produtos-cold-google-search-standard&utm_term=kw-smart-trac&utm_content=sensor%20tractian&gad_source=1&gbraid=0AAAAACa-O1EvPwdM4G_sLXnet12qoc44I&gclid=Cj0KCQjw1um-BhDtARIsABjU5x5cGUp0O52Pq96BNr1A7KVHDvs-k5lWy92qnTboZFFfdOZk7Ei9hwEaAiykEALw_wcB

https://www.youtube.com/watch?v=tgjnD_j2iPE

https://fcc.report/FCC-ID/2BCIS-ST-ULTRA/7118255

Sensores:
https://www.manualdomaker.com/article/sensor-de-poeira-e-fumaca-dsm501a/ .
https://d229kd5ey79jzj.cloudfront.net/974/MPU-6000-Datasheet1.pdf/ .
https://www.bluemakers.com.br/suprimentos/termistor-ntc-100k-3950-cabo-1m-conector-dupont/ .

## 📜 Licença
Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
