import streamlit as st
import json
import requests

# Configuração da página e visualização mobile
st.set_page_config(
    page_title="Guru das Múltiplas - Estatísticas e Palpites",
    page_icon="🔮",
    layout="wide"
)

# Estilização CSS limpa para o tema Guru Premium (Roxo, Azul Neon e Dourado)
style_css = """
<style>
.main { background-color: #0d0e15; color: #f1f1f7; }
.stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #141622; padding: 10px; border-radius: 12px; }
.stTabs [data-baseweb="tab"] { color: #8e94a6 !important; font-weight: bold; background-color: transparent; border: none; padding: 10px 20px; border-radius: 8px; transition: 0.3s; }
.stTabs [aria-selected="true"] { color: #a855f7 !important; background-color: #241938 !important; border-bottom: 2px solid #a855f7 !important; }

.header-box { background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); padding: 30px; border-radius: 16px; border: 1px solid #a855f7; text-align: center; margin-bottom: 25px; box-shadow: 0 8px 32px 0 rgba(168, 85, 247, 0.2); }
.header-box h1 { color: #ffffff; font-size: 32px; font-weight: 800; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
.header-box p { color: #c084fc; font-size: 16px; margin: 0; font-weight: 500; }

.update-tag { background-color: #1e1b4b; border: 1px solid #3b82f6; color: #60a5fa; padding: 6px 14px; border-radius: 30px; font-size: 13px; font-weight: bold; display: inline-block; margin-top: 15px; }

.bilhete-card { background-color: #141622; border-radius: 14px; border-left: 5px solid #a855f7; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
.bilhete-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #24273a; padding-bottom: 12px; margin-bottom: 15px; }
.bilhete-titulo { font-size: 18px; font-weight: bold; color: #ffffff; margin: 0; }

.badge-odd { background: linear-gradient(135deg, #ca8a04 0%, #eab308 100%); color: #000000; font-weight: 900; padding: 5px 12px; border-radius: 8px; font-size: 15px; }
.badge-prob { background-color: #1e1b4b; color: #a855f7; border: 1px solid #a855f7; font-weight: bold; padding: 5px 12px; border-radius: 8px; font-size: 14px; margin-right: 8px; }

.jogo-item { background-color: #1b1e2e; padding: 12px 16px; border-radius: 10px; margin-bottom: 8px; border: 1px solid #24273a; display: flex; justify-content: space-between; align-items: center; }
.jogo-info { display: flex; flex-direction: column; }
.jogo-times { font-size: 15px; font-weight: bold; color: #ffffff; }
.jogo-detalhes { font-size: 12px; color: #8e94a6; margin-top: 2px; }
.jogo-mercado { background-color: #241938; color: #c084fc; border: 1px solid #581c87; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: bold; text-align: right; }
.jogo-odd { font-weight: bold; color: #eab308; font-size: 14px; margin-left: 8px; }

.app-install-box { background-color: #141622; border: 1px dashed #3b82f6; padding: 15px; border-radius: 12px; text-align: center; margin-top: 30px; }
</style>
"""

st.markdown(style_css, unsafe_allow_html=True)

# URL do JSON bruto no seu repositório
JSON_URL = "https://raw.githubusercontent.com/rochapereira1970-svg/GURU-DAS-MULTIPLAS/main/jogos_guru.json"

def carregar_dados():
    try:
        resposta = requests.get(JSON_URL)
        if resposta.status_code == 200:
            return json.loads(resposta.text)
    except:
        pass
    return None

dados = carregar_dados()

# Banner Principal do Aplicativo
data_atualizacao = dados['ultima_atualizacao'] if dados else "Aguardando atualização..."
st.markdown(f"""
    <div class="header-box">
        <h1>🔮 GURU DAS MÚLTIPLAS</h1>
        <p>Bilhetes Estratégicos Baseados em Análise de Dados de Alta Probabilidade</p>
        <div class="update-tag">🔄 Atualizado em: {data_atualizacao}</div>
    </div>
""", unsafe_allow_html=True)

if not dados:
    st.warning("O robô está processando as estatísticas do dia. Volte em instantes!")
else:
    # Criação das Abas principais
    aba_free, aba_vip = st.tabs(["🟢 BILHETES FREE", "👑 ACESSO VIP (GURU)"])

    # --- ABA FREE ---
    with aba_free:
        st.markdown("<p style='color:#8e94a6; font-size:14px; margin-bottom: 20px;'>Abaixo estão suas sugestões gratuitas de hoje com probabilidade matemática calculada acima de 78%:</p>", unsafe_allow_html=True)
        
        for bilhete in dados.get("bilhetes_free", []):
            st.markdown(f"""
                <div class="bilhete-card">
                    <div class="bilhete-header">
                        <span class="bilhete-titulo">{bilhete['tipo']}</span>
                        <div>
                            <span class="badge-prob">🎯 Probabilidade: {bilhete['probabilidade']}</span>
                            <span class="badge-odd">ODD: {bilhete['odds_total']}</span>
                        </div>
                    </div>
            """, unsafe_allow_html=True)
            
            for jogo in bilhete.get("jogos", []):
                st.markdown(f"""
                    <div class="jogo-item">
                        <div class="jogo-info">
                            <span class="jogo-times">{jogo['time_casa']} x {jogo['time_fora']}</span>
                            <span class="jogo-detalhes">🏆 {jogo['campeonato']}</span>
                        </div>
                        <div>
                            <span class="jogo-mercado">{jogo['mercado']}</span>
                            <span class="jogo-odd">@{jogo['odd_jogo']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- ABA VIP ---
    with aba_vip:
        st.markdown("<p style='color:#8e94a6; font-size:14px; margin-bottom: 20px;'>Área exclusiva para assinantes premium. Digite sua chave de acesso para liberar 5 bilhetes extras todos os dias.</p>", unsafe_allow_html=True)
        
        # Sistema simples de bloqueio por senha
        senha = st.text_input("Insira sua Chave de Acesso VIP:", type="password", placeholder="Digite aqui sua senha...")
        
        if senha == "VIP2026":
            st.success("Acesso VIP Liberado! O Guru preparou as melhores combinações para você lucrar alto hoje:")
            
            for bilhete in dados.get("bilhetes_vip", []):
                st.markdown(f"""
                    <div class="bilhete-card" style="border-left-color: #ca8a04;">
                        <div class="bilhete-header">
                            <span class="bilhete-titulo" style="color: #eab308;">{bilhete['tipo']}</span>
                            <div>
                                <span class="badge-prob" style="color:#eab308; border-color:#ca8a04; background-color:#2a2315;">🎯 Probabilidade: {bilhete['probabilidade']}</span>
                                <span class="badge-odd">ODD: {bilhete['odds_total']}</span>
                            </div>
                        </div>
                """, unsafe_allow_html=True)
                
                for jogo in bilhete.get("jogos", []):
                    st.markdown(f"""
                        <div class="jogo-item">
                            <div class="jogo-info">
                                <span class="jogo-times">{jogo['time_casa']} x {jogo['time_fora']}</span>
                                <span class="jogo-detalhes">🏆 {jogo['campeonato']}</span>
                            </div>
                            <div>
                                <span class="jogo-mercado" style="background-color:#2a2315; color:#eab308; border-color:#ca8a04;">{jogo['mercado']}</span>
                                <span class="jogo-odd">@{jogo['odd_jogo']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        elif senha != "":
            st.error("Chave de acesso inválida ou expirada. Verifique com o administrador.")

# Rodapé instrutivo para transformar o painel em WebApp Mobile
st.markdown("""
    <div class="app-install-box">
        <span style="color: #60a5fa; font-weight: bold; font-size: 14px;">📲 Use como um Aplicativo no Celular!</span><br>
        <span style="color: #8e94a6; font-size: 12px;">No Android clique nos 3 pontinhos do Chrome e escolha "Instalar aplicativo". No iPhone clique em compartilhar no Safari e escolha "Adicionar à Tela de Início".</span>
    </div>
""", unsafe_allow_html=True)
