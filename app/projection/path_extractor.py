class PathExtractor:
    @staticmethod
    def extract(obj, path: str):
        """
        Extracts a value from obj using a dot-notation path.
        Supports:
        - Nested attributes/keys: location.city
        - List indexing: emails[0]
        - List mapping: skills[].name
        """
        if not path:
            return None
        
        parts = path.split('.')
        current = obj
        
        for i, part in enumerate(parts):
            if current is None:
                return None
            
            # Handle list indexing or mapping like emails[0] or skills[]
            if '[' in part and part.endswith(']'):
                base_name = part[:part.index('[')]
                index_str = part[part.index('[')+1:-1]
                
                if base_name:
                    if isinstance(current, dict):
                        current_list = current.get(base_name, [])
                    else:
                        current_list = getattr(current, base_name, [])
                else:
                    current_list = current # Handle case where current is already a list and path is "[]"
                
                if not isinstance(current_list, list):
                    return None
                    
                if not current_list:
                    return None
                    
                if index_str == '':
                    # Array mapping
                    remaining_path = '.'.join(parts[i+1:])
                    if not remaining_path:
                        return current_list
                    
                    # Extract from all items, filter out Nones if desired, but typically we just map
                    result = []
                    for item in current_list:
                        if item is not None:
                            val = PathExtractor.extract(item, remaining_path)
                            if val is not None:
                                result.append(val)
                    return result
                else:
                    # Specific index
                    try:
                        idx = int(index_str)
                        current = current_list[idx]
                    except (ValueError, IndexError):
                        return None
            else:
                # Normal attribute or dict key
                if isinstance(current, dict):
                    current = current.get(part, None)
                else:
                    current = getattr(current, part, None)
                    
        return current
