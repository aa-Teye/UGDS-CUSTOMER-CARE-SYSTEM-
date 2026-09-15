"""
Arkesel SMS integration module.
Handles sending SMS messages via the Arkesel v2 API.
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger("ugds-watcher")

ARKESEL_SEND_URL = "https://sms.arkesel.com/api/v2/sms/send"
ARKESEL_BALANCE_URL = "https://sms.arkesel.com/api/v2/clients/balance-details"

class ArkeselSMSService:
    def __init__(self, api_key: str, sender_id: str = "UGDS", dry_run: bool = True):
        self.api_key = api_key
        self.sender_id = sender_id or "UGDS"
        self.dry_run = dry_run

    def check_balance(self) -> Optional[Dict[str, Any]]:
        """Checks SMS balance on the Arkesel account."""
        if not self.api_key or self.dry_run:
            return {"status": "mock", "sms_balance": "N/A (Dry Run)"}

        try:
            headers = {"api-key": self.api_key}
            resp = requests.get(ARKESEL_BALANCE_URL, headers=headers, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                logger.warning(f"Could not retrieve Arkesel balance: {resp.status_code} - {resp.text}")
                return None
        except Exception as e:
            logger.error(f"Error checking Arkesel balance: {e}")
            return None

    def send_sms(self, phone_number: str, message: str) -> Dict[str, Any]:
        """
        Sends an SMS to a single recipient (or simulates if dry_run=True).
        phone_number must be E.164 without plus: 233XXXXXXXXX.
        """
        if self.dry_run:
            logger.info(f"[DRY-RUN SIMULATION] SMS to {phone_number} from '{self.sender_id}': \"{message}\"")
            return {
                "status": "DRY_RUN",
                "message": "Simulated send (DRY_RUN=True)",
                "recipient": phone_number
            }

        if not self.api_key:
            err = "ARKESEL_API_KEY is not configured in .env!"
            logger.error(err)
            return {"status": "FAILED", "error": err}

        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "sender": self.sender_id,
            "message": message,
            "recipients": [phone_number]
        }

        # Try Arkesel v2 first
        try:
            resp = requests.post(ARKESEL_SEND_URL, json=payload, headers=headers, timeout=15)
            resp_data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {"raw": resp.text}

            if resp.status_code in (200, 201):
                logger.info(f"SMS successfully dispatched to {phone_number}. Response: {resp_data}")
                return {"status": "SENT", "response": resp_data}

            # If v2 fails with auth error, try v1 legacy endpoint as fallback
            v1_url = (
                f"https://sms.arkesel.com/sms/api?action=send-sms"
                f"&api_key={self.api_key}&to={phone_number}&from={self.sender_id}&sms={requests.utils.quote(message)}"
            )
            v1_resp = requests.get(v1_url, timeout=15)
            v1_data = v1_resp.json() if v1_resp.headers.get("content-type", "").startswith("application/json") else {"raw": v1_resp.text}
            if v1_resp.status_code == 200 and "error" not in v1_resp.text.lower() and "failed" not in v1_resp.text.lower():
                logger.info(f"SMS successfully dispatched via v1 to {phone_number}. Response: {v1_data}")
                return {"status": "SENT", "response": v1_data}

            logger.error(f"Arkesel returned error (v2: {resp.status_code} {resp_data}, v1: {v1_resp.status_code} {v1_data})")
            return {"status": "FAILED", "response": resp_data, "v1_response": v1_data}
        except Exception as exc:
            logger.error(f"Network error sending SMS to {phone_number}: {exc}")
            return {"status": "FAILED", "error": str(exc)}

