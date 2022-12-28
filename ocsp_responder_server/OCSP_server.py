from werkzeug.serving import run_simple
import openssl_ocsp_responder
import datetime
import argparse
from .rpc_server_request import RPCServerRequest

OCSP_DIR = "ocsp_files"
OCSP_CA_CERT_PATH = f"{OCSP_DIR}/intermediate_ca_cert.pem"
OCSP_CERT_PATH = f"{OCSP_DIR}/ocsp_cert.pem"
OCSP_KEY_PATH = f"{OCSP_DIR}/ocsp_key.pem"
PROXY_CERT_PATH = f"{OCSP_DIR}/proxy_cert.pem"

OCSP_SERVER_PORT = 10001
OCSP_RESPONDER_PORT = 10002


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ca_certificate_path",
        required=True,
        type=str,
        help="Path to the certificate PEM file for the CA that " "issued the certificates the responder has to approve",
    )
    parser.add_argument(
        "--ocsp_certificate_path", required=True, type=str, help="Path to the OCSP Responder's certificate PEM file"
    )
    parser.add_argument(
        "--ocsp_key_path", required=True, type=str, help="Path to the OCSP Responder's private key file"
    )
    parser.add_argument("--port", required=True, type=int, help="Port the responder should listen to")
    parser.add_argument(
        "--crl_dir", required=False, type=str, default="./", help="The path to the directory to write the CRL file in"
    )
    parser.add_argument(
        "--log_output_path",
        required=False,
        type=str,
        default="./out",
        help="Absolute path to an output file for the responder",
    )
    parser.add_argument(
        "--request_timeout",
        required=False,
        type=float,
        default=0.8,
        help="Timeout in seconds for sending a single OCSP request to the responder",
    )
    parser.add_argument(
        "--total_timeout",
        required=False,
        type=float,
        default=5,
        help="Timeout in seconds for when polling the responder " "itself for a status of a certificate",
    )
    return parser.parse_args()


class OCSPResponderHandler(object):
    def __init__(self, ocsp_config_input):
        self.OCSP_responder = openssl_ocsp_responder.OCSPResponder(**ocsp_config_input)

        self._to_dispatch = {
            "start_responder": self.start_responder,
            "is_alive": self.is_alive,
            "stop_responder": self.stop_responder,
            "restart": self.restart,
            "delete_crl_file": self.delete_crl_file,
            "write_crl": self.write_crl,
            "set_verified_certificate": self.set_verified_certificate,
            "set_revoked_certificate": self.set_revoked_certificate,
            "delete_certificate": self.delete_certificate,
            "get_status": self.get_status,
        }

    @property
    def to_dispatch(self):
        return self._to_dispatch

    def start_responder(self):
        self.OCSP_responder.start_responder()

    def is_alive(self):
        return {"is_alive": self.OCSP_responder.is_alive()}

    def stop_responder(self):
        self.OCSP_responder.stop_responder()

    def restart(self):
        self.OCSP_responder.restart()

    def delete_crl_file(self):
        self.OCSP_responder.delete_crl_file()

    def write_crl(self):
        self.OCSP_responder.write_crl()

    def set_verified_certificate(self, certificate_path):
        self.OCSP_responder.set_verified_certificate(certificate_path)

    def set_revoked_certificate(self, certificate_path, revocation_time=None):
        if revocation_time:
            revocation_time = datetime.datetime.strptime(revocation_time, "%d%m%y%H%M%SZ")
        self.OCSP_responder.set_revoked_certificate(certificate_path, revocation_time)

    def delete_certificate(self, certificate_path):
        self.OCSP_responder.delete_certificate(certificate_path)

    def get_status(self, certificate_path, issuer_certificate_path, request_timeout=None, total_timeout=None):
        return {
            "ocsp_status": str(
                self.OCSP_responder.get_status(
                    certificate_path, issuer_certificate_path, request_timeout, total_timeout
                )
            )
        }


if __name__ == "__main__":
    dispatcher = RPCServerRequest()
    ocsp = OCSPResponderHandler(vars(arg_parser()))
    dispatcher.register(**ocsp.to_dispatch)
    run_simple("", OCSP_SERVER_PORT, dispatcher.application)
