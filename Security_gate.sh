apt-get update && apt-get install -y jq
highs=$(jq '[.results[] | select(.issue_severity == "HIGH")] | length' bandit_report.json)
mediums=$(jq '[.results[] | select(.issue_severity == "MEDIUM")] | length' bandit_report.json)
echo "Numero de HIGH VULNERABILITIES: $highs"
echo "\nNumero de MEDIUM VULNERABILITIES: $mediums"
if [ "$highs" -gt 0 ]; then
  echo "Hay más de 1 vulnerabilidades HIGH. Fallando la build."
  exit 1
fi
