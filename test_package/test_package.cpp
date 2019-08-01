#include <cstdlib>
#include <iostream>
#include "cassandra.h"

int main()
{
    CassUuidGen* uuid_gen = cass_uuid_gen_new();
    CassUuid uuid;

    cass_uuid_gen_random(uuid_gen, &uuid);
    char uuid_str[CASS_UUID_STRING_LENGTH];
    cass_uuid_string(uuid, uuid_str);

    std::cout << uuid_str << std::endl;
}
