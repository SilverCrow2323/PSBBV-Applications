#ifndef PSBBV_APPLICATION_CATALOGUE_H
#define PSBBV_APPLICATION_CATALOGUE_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
#define PSBBV_APP_CATALOGUE_CAPACITY 128u
#define PSBBV_APP_TITLE_ID_SIZE 10u
#define PSBBV_APP_TITLE_SIZE 96u
#define PSBBV_APP_VERSION_SIZE 32u
typedef enum { PSBBV_APP_OK=0, PSBBV_APP_INVALID, PSBBV_APP_DUPLICATE, PSBBV_APP_FULL } psbbv_app_result;
typedef struct {
    char title_id[PSBBV_APP_TITLE_ID_SIZE];
    char title[PSBBV_APP_TITLE_SIZE];
    char version[PSBBV_APP_VERSION_SIZE];
} psbbv_app_record;
typedef struct { psbbv_app_record records[PSBBV_APP_CATALOGUE_CAPACITY]; size_t count; } psbbv_app_catalogue;
void psbbv_app_catalogue_init(psbbv_app_catalogue *catalogue);
psbbv_app_result psbbv_app_catalogue_add(psbbv_app_catalogue *catalogue,const char *title_id,const char *title,const char *version);
const psbbv_app_record *psbbv_app_catalogue_find(const psbbv_app_catalogue *catalogue,const char *title_id);
#ifdef __cplusplus
}
#endif
#endif
