#include "psbbv/applications/catalogue.h"
#include <string.h>
static int valid_title_id(const char *id) {
    size_t i;
    if (!id || strlen(id)!=9) return 0;
    for (i=0;i<9;i++) if (!((id[i]>='A'&&id[i]<='Z')||(id[i]>='0'&&id[i]<='9'))) return 0;
    return 1;
}
static int copy_field(char *dst,size_t cap,const char *src) {
    size_t n;
    if (!src || !src[0]) return 0;
    n=strlen(src); if (n>=cap) return 0;
    memcpy(dst,src,n+1); return 1;
}
void psbbv_app_catalogue_init(psbbv_app_catalogue *c) { if(c) memset(c,0,sizeof(*c)); }
const psbbv_app_record *psbbv_app_catalogue_find(const psbbv_app_catalogue *c,const char *id) {
    size_t i; if(!c||!id) return NULL;
    for(i=0;i<c->count;i++) if(strcmp(c->records[i].title_id,id)==0) return &c->records[i];
    return NULL;
}
psbbv_app_result psbbv_app_catalogue_add(psbbv_app_catalogue *c,const char *id,const char *title,const char *version) {
    psbbv_app_record item;
    if(!c||!valid_title_id(id)||!title||!title[0]||!version||!version[0]) return PSBBV_APP_INVALID;
    if(psbbv_app_catalogue_find(c,id)) return PSBBV_APP_DUPLICATE;
    if(c->count>=PSBBV_APP_CATALOGUE_CAPACITY) return PSBBV_APP_FULL;
    memset(&item,0,sizeof(item));
    if(!copy_field(item.title_id,sizeof(item.title_id),id)||!copy_field(item.title,sizeof(item.title),title)||!copy_field(item.version,sizeof(item.version),version)) return PSBBV_APP_INVALID;
    c->records[c->count++]=item; return PSBBV_APP_OK;
}
