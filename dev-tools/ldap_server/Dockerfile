FROM osixia/openldap:1.5.0

ENV LDAP_ORGANISATION="Hogwarts School of Witchcraft and Wizardry"
ENV LDAP_DOMAIN="hogwarts.ac.uk"
ENV LDAP_ADMIN_PASSWORD="admin"
ENV LDAP_CONFIG_PASSWORD="admin"
ENV LDAP_TLS="false"
ENV LDAP_TLS_VERIFY_CLIENT="never"

ARG bootstrap_dir=/container/service/slapd/assets/config/bootstrap/ldif
RUN mkdir -p $bootstrap_dir
COPY ./seed.ldif $bootstrap_dir

# Used to simluate LDAP locally.

# Server URI:       ldap://localhost:389
# Base DN:          dc=hogwarts,dc=ac,dc=uk
# User filter:      uid={username}
# Auth DN:          cn=admin,dc=hogwarts,dc=ac,dc=uk
# Auth Password:    admin

# Admin group:      cn=tmr-admins,ou=groups,dc=hogwarts,dc=ac,dc=uk
# --> dumbledore (password: "krembo" -- get the reference?) is the only member of this group

# Users group:      cn=tmr-users,ou=groups,dc=hogwarts,dc=ac,dc=uk
# --> harry (password: "password") is the only member of this group
