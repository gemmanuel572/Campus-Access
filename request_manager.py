import json
import os
import re


requests = []


def create_request(fellow_id, card_type):
    if not isinstance(fellow_id, str) or not fellow_id.strip():
        raise ValueError("Fellow ID cannot be empty.")

    if card_type not in ("visitor", "student", "staff"):
        raise ValueError("Invalid card type.")

    request_id = generate_request_id()

    request = {
        "id": request_id,
        "fellow_id": fellow_id.strip(),
        "card_type": card_type,
        "status": "requested",
        "approved_by": None,
    }

    requests.append(request)
    return request.copy()


def generate_request_id():
    highest_id = 0

    for request in requests:
        request_id = request["id"]

        if re.fullmatch(r"A[0-9]{3,}", request_id):
            highest_id = max(highest_id, int(request_id[1:]))

    return f"A{highest_id + 1:03d}"


def get_request(request_id):
    for request in requests:
        if request["id"] == request_id:
            return request.copy()

    return None


def save_requests(path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(requests, file, indent=4)


def load_requests(path):
    global requests

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Invalid data: expected a list of requests.")

    required_fields = {
        "id",
        "fellow_id",
        "card_type",
        "status",
        "approved_by",
    }
    seen_ids = set()

    for request in data:
        if not isinstance(request, dict) or set(request.keys()) != required_fields:
            raise ValueError("Invalid request structure.")

        request_id = request["id"]

        if (
            not isinstance(request_id, str)
            or re.fullmatch(r"A[0-9]{3,}", request_id) is None
        ):
            raise ValueError(f"Invalid request ID: {request_id}")

        if request_id in seen_ids:
            raise ValueError(f"Duplicate request ID: {request_id}")
        seen_ids.add(request_id)

        if not isinstance(request["fellow_id"], str) or not request["fellow_id"].strip():
            raise ValueError("Invalid fellow ID.")

        if request["card_type"] not in ("visitor", "student", "staff"):
            raise ValueError("Invalid card type.")

        if request["status"] not in (
            "requested",
            "approved",
            "issued",
            "returned",
        ):
            raise ValueError("Invalid request status.")

        if request["status"] == "requested" and request["approved_by"] is not None:
            raise ValueError("Requested items cannot have an approver.")

        if request["status"] in ("approved", "issued", "returned"):
            if not isinstance(request["approved_by"], str) or not request["approved_by"].strip():
                raise ValueError("Approved, issued, and returned requests need an approver.")

    requests = [request.copy() for request in data]