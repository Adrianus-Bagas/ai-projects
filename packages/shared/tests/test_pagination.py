from shared.schemas.pagination import PaginationParams

params = PaginationParams(page=1, page_size=10)

print(params.page)
print(params.page_size)
print(params.offset)