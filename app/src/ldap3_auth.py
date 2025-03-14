"""
ldap3_auth.py
v1.0.0, 3/14/2025
Branch: fredhutch-deployment
Author: Dan Tenenbaum, scicomp@fredhutch.org
Maintainer: Alexander Netzley, anetzley@fredhutch.org
Scientific Computing, Fred Hutchinson Cancer Research Center

This module provides the logic for checking user authentication within the Fred Hutch network.
"""
import ldap3
from ldap3.core.exceptions import LDAPInvalidCredentialsResult


def authenticate(username, password):
    """
    Determine whether hutchnet ID & password are valid.
    Only works inside Hutch network (which is good!).
    """

    if not password:
        return False

    server = ldap3.Server("dc.fhcrc.org", port=636, use_ssl=True, get_info=ldap3.ALL)
    try:
        conn = ldap3.Connection(
            server,
            authentication=ldap3.SIMPLE,
            user=f"{username}@fhcrc.org",
            password=password,
            check_names=True,
            lazy=False,
            client_strategy=ldap3.SYNC,
            raise_exceptions=True,
        )
        conn.open()
        conn.bind()
        return True
    except LDAPInvalidCredentialsResult:
        return False
    return False