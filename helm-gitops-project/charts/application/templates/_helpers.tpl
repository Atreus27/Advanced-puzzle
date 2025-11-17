{{/* vim: set filetype=mustache: */}}

{{/*
Expand the name of the chart.
*/}}
{{- define "application.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "application.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "application.service.name" -}}
{{- printf "%s" (include "application.fullname" .) -}}
{{- end -}}

{{- define "application.ingress.hosts" -}}
{{- if .Values.ingress.hosts }}
{{- $hosts := .Values.ingress.hosts }}
{{- range $i, $host := $hosts }}
{{ $host }}{{- if lt $i (sub (len $hosts) 1) }},{{ end }}
{{- end }}
{{- end }}
{{- end }}

{{- define "application.labels" -}}
app: {{ include "application.fullname" . }}
{{- end }}
