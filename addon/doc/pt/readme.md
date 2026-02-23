# WhatsApp NG

Complemento NVDA que fornece melhorias de acessibilidade para o WhatsApp Desktop baseado na web.

## Recursos

- **Alt+1**: Ir para a lista de conversas do WhatsApp
- **Alt+2**: Ir para a lista de mensagens do WhatsApp
- **Alt+D**: Focar no campo de entrada de mensagens
- **Enter**: Reproduzir mensagem de voz (funciona em conversas individuais e grupos)
- **Shift+Enter**: Abrir menu de contexto da mensagem
- **Control+C**: Copiar mensagem atual para a área de transferência
- **Control+R**: Ler mensagem completa (clica no botão "ler mais" se necessário)

### Scripts de Alternância (sem atalho padrão - configure em Gestos de Entrada)

- Alternar filtragem de números de telefone na lista de conversas
- Alternar filtragem de números de telefone na lista de mensagens
- Alternar Modo de Foco automático (permite usar Browse Mode quando necessário)

## Requisitos

- NVDA 2021.1 ou posterior
- WhatsApp Desktop (versão baseada na web)

## Instalação

1. Baixe o arquivo `whatsAppNG.nvda-addon`
2. No NVDA, vá em **Ferramentas → Gerenciador de Complementos**
3. Clique em **Instalar** e selecione o arquivo
4. Reinicie o NVDA

## Configuração

Os filtros de números de telefone podem ser alternados:
- Na lista de conversas: Configure um atalho em Gestos de Entrada
- Na lista de mensagens: Configure um atalho em Gestos de Entrada

Configure os atalhos em:
**Menu NVDA → Preferências → Gestos de Entrada → WhatsApp NG**

## Registro de Alterações

### Versão 1.4.0 (2026-02-23)

**Adicionado:**
- Suporte completo aos seguintes idiomas: Árabe, Alemão, Espanhol, Italiano e Russo
- Tradução ucraniana atualizada com as strings mais recentes

**Corrigido:**
- Erro "Texto não encontrado" no Control+R após clicar no botão "ler mais"
- Control+R agora funciona apenas em mensagens de texto (exibe "Não é uma mensagem de texto" para voz/imagens)

**Alterado:**
- Links do repositório atualizados para o novo local (nunotfc/WhatsAppNG)
- Documentação: Todos os READMEs localizados agora incluem o changelog completo até a versão 1.3.0

### Versão 1.3.0 (2026-02-07)

**Adicionado:**
- Suporte à tradução turca
- Opção para alternar Modo de Foco automático (configure o gesto em Gestos de Entrada)

**Alterado:**
- Performance melhorada: Comandos de navegação agora são mais rápidos em usos repetidos
- Tecla Escape agora passa corretamente para o WhatsApp

**Corrigido:**
- Enter agora reproduz mensagens de vídeo (anteriormente funcionava apenas para áudio)

### Versão 1.1.1 (2025-01-31)

**Adicionado:**
- Control+R: Ler mensagem completa (clica automaticamente no botão "ler mais")
- Control+C: Copiar mensagem atual para a área de transferência
- Desativação automática do modo de navegação (mantém o modo de foco ativo para melhor experiência no WhatsApp)

**Alterado:**
- Mensagens de erro melhoradas: Todos os scripts agora fornecem feedback claro em caso de falha
- Comandos de navegação (Alt+1, Alt+2, Alt+D) agora silenciosos em caso de sucesso
- Enter: Detecção baseada em controle deslizante em vez de contar botões (mais confiável)

**Corrigido:**
- Alt+1 e Alt+2 relatam erros corretamente quando todos os caminhos falham
- Otimizada filtragem de objetos para reduzir latência de entrada

### Versão 1.1.0 (2025-01-30)

**Adicionado:**
- Control+R: Ler mensagem completa
- Reprodução inteligente de mensagem de voz usando detecção de controle deslizante

**Alterado:**
- Enter: Lógica melhorada usando detecção de controle deslizante em vez de contar botões

**Corrigido:**
- Alt+2 agora tenta corretamente todos os caminhos de navegação se a primeira tentativa falhar

### Versão 1.0.0 (2025-01-29)

**Lançamento inicial:**
- Atalhos de navegação para lista de conversas, lista de mensagens e campo de mensagem
- Reprodução de mensagens de voz com suporte para conversas individuais e grupos
- Acesso ao menu de contexto para ações de mensagem
- Alternância de filtragem de números de telefone para conversas e mensagens
- Ativação automática do modo de foco no WhatsApp Desktop

## Créditos

Desenvolvido por Nuno Costa para fornecer melhorias de acessibilidade para a experiência moderna do WhatsApp Desktop.

## Suporte

Para problemas ou sugestões, visite:
https://github.com/nunotfc/whatsAppNG/issues

## Compilação de Traduções

Para atualizar ou compilar traduções:
```bash
scons pot
```

Isso requer que as ferramentas GNU Gettext estejam instaladas.
