#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

execdir="$(realpath "$(dirname "$0")")"

endpoint="YOUR_COMMON_NAME"
public_file=self_signed_cert.der
private_file=cprik.der
credentials_file=credentials.c
keys_file=keys.pem

args_list="credentials:,endpoint:,keys:,private:.public:"

args=$(getopt -o+ho:x -l $args_list -n "$(basename "$0")" -- "$@")
eval set -- "$args"

while [ $# -gt 0 ]; do
  if [ -n "${opt_prev:-}" ]; then
    eval "$opt_prev=\$1"
    opt_prev=
    shift 1
    continue
  elif [ -n "${opt_append:-}" ]; then
    eval "$opt_append=\"\${$opt_append:-} \$1\""
    opt_append=
    shift 1
    continue
  fi
  case $1 in
  --credentials)
    opt_prev=credentials_file
    ;;

  --endpoint)
    opt_prev=endpoint
    ;;

  --keys)
    opt_prev=keys_file
    ;;

  --private)
    opt_prev=private_file
    ;;

  --public)
    opt_prev=public_file
    ;;

  esac
  shift 1
done


set -x

openssl ecparam -out ${keys_file} -name prime256v1 -genkey
openssl pkcs8 -topk8 -inform PEM -outform DER -in ${keys_file} -out ${private_file} -nocrypt
openssl req -x509 -new -key ${keys_file} -sha256 -days 36500 -subj "/CN=${endpoint}" -outform DER -out ${public_file}

"${execdir}/cert_convert.py" --public ${public_file} --private ${private_file} --out ${credentials_file}

set +x
