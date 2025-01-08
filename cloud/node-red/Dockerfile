# Dockerfile.nodered
FROM nodered/node-red:4.0.8-22

# Utiliser l'utilisateur node-red créé par node red
USER node-red

RUN npm install utf-8-validate \
    && npm install bufferutil \
    && npm install node-red-dashboard \
    && npm install node-red-node-ui-table

# Démarrer Node-RED
CMD ["npm", "start", "--", "--userDir", "/data"]
