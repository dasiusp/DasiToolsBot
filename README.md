# Dasitools
Bot no telegram para marcar todos os membros de um setor ou todos os membros do Dasi-USP

# Deploy:
	gcloud beta functions deploy webhook --set-env-vars "TELEGRAM_TOKEN=[SECRET]" --runtime python37 --trigger-http
Na GCloud do DASI

Token está no BitWarden do Diretor de T.I.
