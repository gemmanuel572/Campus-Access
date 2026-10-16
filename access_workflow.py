import request_manager as rm


def _find_request(request_id):
    """Return a stored request or reject an unknown ID."""
    if not isinstance(request_id, str):
        raise ValueError("Invalid request ID.")

    for request in rm.requests:
        if request["id"] == request_id:
            return request

    raise ValueError(f"Request {request_id!r} was not found.")


def approve_request(request_id, approved_by):
    """Approve a request and record the approver."""
    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("Approver ID cannot be empty.")

    request = _find_request(request_id)

    if request["status"] != "requested":
        raise ValueError("Only requested cards can be approved.")

    request["status"] = "approved"
    request["approved_by"] = approved_by.strip()

    return request.copy()


def issue_request(request_id):
    """Issue a card only after approval."""
    request = _find_request(request_id)

    if request["status"] != "approved":
        raise ValueError("Only approved cards can be issued.")

    if not isinstance(request["approved_by"], str) or not request["approved_by"].strip():
        raise ValueError("An approver is required before issuing.")

    request["status"] = "issued"

    return request.copy()


def return_request(request_id):
    """Mark an issued card as returned."""
    request = _find_request(request_id)

    if request["status"] != "issued":
        raise ValueError("Only issued cards can be returned.")

    request["status"] = "returned"

    return request.copy()
