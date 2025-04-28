import argparse
import configparser
import os
from os.path import expanduser

def parse_arguments():
    """
    Parses command-line arguments and loads configuration from file.
    Command-line arguments override file settings.
    """
    parser = argparse.ArgumentParser(description='Automatically analyze +45 protocols.')
    # ... (define all your existing arguments here as in the original script)
    
    # Add argument for specifying configuration file
    parser.add_argument('--config', default=expanduser("~") + '/.legion/config.ini',
                        help='Path to the configuration file (Default: ~/.legion/config.ini)')
    
    # Add argument for specifying a profile
    parser.add_argument('--profile', default='DEFAULT',
                        help='Profile to use from the configuration file (Default: DEFAULT)')

    args = parser.parse_args()

    config = configparser.ConfigParser()
    
    # Read the configuration file
    if os.path.exists(args.config):
        config.read(args.config)
    else:
        print(f"[!] Configuration file not found: {args.config}. Using default settings and command-line arguments.")

    # Create a dictionary to hold the final configuration
    # Start with defaults or a specified profile
    if args.profile in config:
        settings = dict(config.items(args.profile))
    else:
        if args.profile != 'DEFAULT':
            print(f"[!] Profile '{args.profile}' not found in config file. Using DEFAULT or command-line arguments.")
        if 'DEFAULT' in config:
             settings = dict(config.items('DEFAULT'))
        else:
             settings = {} # Start empty if no DEFAULT section

    # Override settings with command-line arguments
    # This requires careful handling of argument types
    for arg, value in vars(args).items():
        # Only override if the command-line argument was explicitly provided
        # This is a simplification; a more robust solution would track if an argument
        # came from the command line or its default value.
        # For now, we'll assume None or default argparse values mean not set by user
        # and any other value should override. This might need refinement.
        
        # A better approach would be to parse arguments twice or use a different
        # strategy to distinguish user-provided args from defaults.
        # For this example, we'll just directly use the parsed args, which already
        # contain overrides if provided.

        # However, we should populate the settings dictionary with ALL
        # arguments from the parser, ensuring correct types are handled.
        # This involves mapping argparse argument names to potentially
        # different internal setting names if desired, and handling types.
        
        # Let's refine this: Use the args object populated by argparse
        # as the primary source, but populate it with values from the config
        # *before* parse_args() or carefully merge after.

        # A common pattern is to use a custom Action for argparse or to
        # process args and config in a specific order.

        # Let's try populating args from config *before* final processing,
        # or create a combined configuration object.

        # Simpler approach for demonstration: merge after parsing, handling types.
        # This requires knowing the expected type of each setting.

        # A more robust approach often involves:
        # 1. Define expected configuration structure and types.
        # 2. Load config file into a temporary structure.
        # 3. Parse command-line arguments.
        # 4. Merge config settings into the parsed arguments' namespace, respecting types and command-line precedence.

        pass # We will use the args object directly after parsing for simplicity in this example

    # For this simplified example, we'll just return the args object
    # which now contains values from command line, and we'd manually
    # incorporate config values elsewhere or in a more complex parsing function.
    # A better pattern follows below:

    # --- Revised approach for merging config and args ---
    parser = argparse.ArgumentParser(description='Automatically analyze +45 protocols.')
    # Define arguments without defaults initially if you want config to provide defaults
    parser.add_argument('--proto', help='Protocol to test')
    parser.add_argument('--host', help='Host to test')
    # ... define all other arguments similarly ...
    parser.add_argument('--workdir', help='Working directory')
    parser.add_argument('-p', '--port', type=int, help='Port where the protocol is listening')
    # ... and so on for all arguments ...

    # Add config and profile arguments with defaults
    parser.add_argument('--config', default=expanduser("~") + '/.legion/config.ini',
                        help='Path to the configuration file')
    parser.add_argument('--profile', default='DEFAULT',
                        help='Profile to use from the configuration file')

    # Parse arguments from the command line first
    cmd_line_args, unknown = parser.parse_known_args() # Use parse_known_args to avoid errors on config-only args

    config = configparser.ConfigParser()
    settings = {}

    # Read the configuration file if it exists
    if os.path.exists(cmd_line_args.config):
        config.read(cmd_line_args.config)

        # Load settings from DEFAULT or specified profile
        profile_name = cmd_line_args.profile
        if profile_name in config:
            settings.update(config.items(profile_name))
        elif 'DEFAULT' in config:
             settings.update(config.items('DEFAULT'))
        
        # Convert known types from strings (configparser reads values as strings)
        # This requires knowledge of expected types for each setting
        if 'port' in settings:
            try:
                settings['port'] = int(settings['port'])
            except ValueError:
                print(f"[!] Invalid port value in config: {settings['port']}. Using command-line or default.")
                del settings['port'] # Remove invalid entry

        if 'intensity' in settings:
            try:
                settings['intensity'] = int(settings['intensity'])
            except ValueError:
                print(f"[!] Invalid intensity value in config: {settings['intensity']}. Using command-line or default.")
                del settings['intensity'] # Remove invalid entry
                
        # Add more type conversions as needed for other arguments

    # Create a new Namespace object to hold the merged configuration
    final_config = argparse.Namespace()

    # Populate final_config with settings from the config file
    for key, value in settings.items():
        # Set attributes dynamically, using the converted types
        setattr(final_config, key, value)

    # Now, iterate through the parsed command-line arguments
    # and override values in final_config if they were provided
    # by the user (i.e., not their default argparse value).
    # This part is still tricky with standard argparse if you don't
    # want command-line defaults to override config file values.
    # A common way is to check if the argument source was the command line.
    # However, a simpler approach for merging is to update the final_config
    # with the parsed command-line arguments, as parse_args already handles
    # which values came from the command line.

    # Let's use a simpler merging strategy for demonstration:
    # 1. Parse command-line args (they get priority).
    # 2. Load config file.
    # 3. For each setting in config, if the corresponding arg in parsed args
    #    is still its default value (or a sentinel indicating it wasn't set),
    #    use the value from the config file.

    parser = argparse.ArgumentParser(description='Automatically analyze +45 protocols.')
    # Define arguments with their desired default values from argparse
    parser.add_argument('--proto', default='scanner', help='Protocol to test (Default: "scanner")')
    parser.add_argument('--host', default="127.0.0.1", help='Host to test (Default: 127.0.0.1)')
    parser.add_argument('--workdir', default=expanduser("~")+'/.legion/', help='Working directory (Default: ~/.legion/)')
    parser.add_argument('-p', '--port', type=int, default=0, help='Port where the protocol is listening')
    parser.add_argument('-i', '--intensity', type=int, default=2, help='1-Main checks, 2-Main and more vulns checks (default), 3-Only Service Bruteforce')
    parser.add_argument('-u', '--username', default="", help='Username to use in bruteforce')
    parser.add_argument('-U', '--ulist', default="", help='Usernames to use in bruteforce')
    parser.add_argument('-k', '--password', default="", help='Password to use')
    parser.add_argument('-P', '--plist', default="", help='Passwords to use in bruteforce')
    parser.add_argument('--protohelp', action="store_true", default=False, help='Set to get help of selected protocol')
    parser.add_argument('--notuse', default="", help='Comma separate string of name of tools that you dont want to be used')
    parser.add_argument('--extensions', default="html,txt,php,asp,aspx", help='USED IN HTTP/s: Set valid extensions')
    parser.add_argument('--path', default="", help='USED IN HTTP/s: Set the URL path')
    parser.add_argument('--ipv6', default="", help='USED IN HTTP/s: Used for reverse dns lookup with ipv6')
    parser.add_argument('--domain', default="", help='If possible, set the domain name')
    parser.add_argument('--execonly', default="", help='Exec only this tool')
    parser.add_argument('-r', '--run', action="store_true", default=False, help='Just run the analysis')
    parser.add_argument('-v', '--verbose', action="store_true", default=True, help='Get output when the command finish (default: True)')

    # Add config and profile arguments
    parser.add_argument('--config', default=expanduser("~") + '/.legion/config.ini',
                        help='Path to the configuration file')
    parser.add_argument('--profile', default='DEFAULT',
                        help='Profile to use from the configuration file')

    # Store the original defaults to check if an argument was provided by the user
    # This is a common technique, but can be complex for all argument types.
    # A simpler way might be to parse args, then load config, then iterate
    # through config items and update args if the arg's value is still its default.
    
    # Let's use a straightforward merge after parsing:
    args = parser.parse_args()

    config = configparser.ConfigParser()
    
    # Read the configuration file
    if os.path.exists(args.config):
        config.read(args.config)

    # Load settings from DEFAULT or specified profile into a dictionary
    settings_from_config = {}
    profile_name = args.profile
    if profile_name in config:
        settings_from_config.update(config.items(profile_name))
    elif 'DEFAULT' in config:
         settings_from_config.update(config.items('DEFAULT'))

    # Now, merge settings from config into the args Namespace
    # Only update args if the corresponding argument was NOT provided on the command line.
    # This requires checking if the parsed arg's value is different from its *argparse default*.
    # Argparse doesn't easily expose if an argument was *provided* vs using its default.
    # A common workaround is to set defaults to `None` or a unique sentinel value initially,
    # then populate from config, then let argparse fill in remaining defaults.

    # Alternative and often cleaner approach:
    # 1. Define args without defaults.
    # 2. Parse args with `parse_known_args` to get provided values.
    # 3. Load config and profile settings.
    # 4. Create a new namespace/object, populate it with config settings.
    # 5. Update the object with the values from the *parsed command-line args*.
    # 6. For any arguments not set by config or command line, apply final defaults.

    # Let's illustrate this cleaner approach:

    parser = argparse.ArgumentParser(description='Automatically analyze +45 protocols.')
    # Define arguments without defaults, or with a sentinel value
    parser.add_argument('--proto', help='Protocol to test')
    parser.add_argument('--host', help='Host to test')
    parser.add_argument('--workdir', help='Working directory')
    parser.add_argument('-p', '--port', type=int, help='Port where the protocol is listening')
    parser.add_argument('-i', '--intensity', type=int, help='Intensity level')
    parser.add_argument('-u', '--username', help='Username for bruteforce')
    parser.add_argument('-U', '--ulist', help='Usernames list for bruteforce')
    parser.add_argument('-k', '--password', help='Password')
    parser.add_argument('-P', '--plist', help='Passwords list for bruteforce')
    parser.add_argument('--protohelp', action="store_true", help='Set to get help of selected protocol')
    parser.add_argument('--notuse', help='Comma separated tools to exclude')
    parser.add_argument('--extensions', help='USED IN HTTP/s: Set valid extensions')
    parser.add_argument('--path', help='USED IN HTTP/s: Set the URL path')
    parser.add_argument('--ipv6', help='USED IN HTTP/s: Used for reverse dns lookup with ipv6')
    parser.add_argument('--domain', help='Set the domain name')
    parser.add_argument('--execonly', help='Exec only this tool')
    parser.add_argument('-r', '--run', action="store_true", help='Just run the analysis')
    parser.add_argument('-v', '--verbose', action="store_true", help='Get output when the command finish')

    # Add config and profile arguments with their defaults
    parser.add_argument('--config', default=expanduser("~") + '/.legion/config.ini',
                        help='Path to the configuration file')
    parser.add_argument('--profile', default='DEFAULT',
                        help='Profile to use from the configuration file')

    # Parse only the arguments that were provided on the command line
    cmd_line_overrides, unknown = parser.parse_known_args()

    config = configparser.ConfigParser()
    settings_from_config = {}

    # Read the configuration file if it exists
    if os.path.exists(cmd_line_overrides.config):
        config.read(cmd_line_overrides.config)

        # Load settings from DEFAULT or specified profile into a dictionary
        profile_name = cmd_line_overrides.profile
        if profile_name in config:
            settings_from_config.update(config.items(profile_name))
        elif 'DEFAULT' in config:
             settings_from_config.update(config.items('DEFAULT'))

        # Perform type conversions for settings loaded from the config file
        # This requires a mapping of setting names to types
        type_conversions = {
            'port': int,
            'intensity': int,
            'protohelp': lambda x: x.lower() == 'true', # Example for boolean
            'run': lambda x: x.lower() == 'true', # Example for boolean
            'verbose': lambda x: x.lower() == 'true', # Example for boolean
            'notuse': lambda x: x.split(','), # Example for list
            'extensions': lambda x: x.split(',') # Example for list
            # Add more conversions as needed
        }
        
        converted_settings_from_config = {}
        for key, value in settings_from_config.items():
            if key in type_conversions:
                try:
                    converted_settings_from_config[key] = type_conversions[key](value)
                except ValueError:
                    print(f"[!] Warning: Could not convert config value '{value}' for setting '{key}'. Skipping.")
            else:
                converted_settings_from_config[key] = value

        settings_from_config = converted_settings_from_config


    # Create a Namespace with final default values (these are the ultimate fallbacks)
    # These should match the original script's default behaviors
    final_config = argparse.Namespace(
        proto='scanner',
        host="127.0.0.1",
        workdir=expanduser("~")+'/.legion/',
        port=0,
        intensity=2,
        username="",
        ulist="",
        password="",
        plist="",
        protohelp=False,
        notuse=[], # Default as empty list
        extensions="html,txt,php,asp,aspx", # Keep as string or convert to list here?
        path="",
        ipv6="",
        domain="",
        execonly="",
        run=False,
        verbose=True,
        config=expanduser("~") + '/.legion/config.ini', # Default for config file path
        profile='DEFAULT' # Default for profile name
    )
    
    # Convert default extensions string to list to match expected type if needed later
    final_config.extensions = final_config.extensions.split(',')
    # Convert default notuse string to list
    final_config.notuse = final_config.notuse[0].split(',') if final_config.notuse else []


    # Update final_config with settings loaded from the config file
    # These override the ultimate fallbacks
    for key, value in settings_from_config.items():
         if hasattr(final_config, key): # Only update if it's a recognized argument
            setattr(final_config, key, value)


    # Update final_config with values provided on the command line
    # These override both fallbacks and config file settings
    # Iterate through the command_line_overrides. We need to know
    # if an argument was *actually provided* on the command line.
    # A common way is to compare with the default that argparse would assign
    # if the argument wasn't present. This is complex.

    # Simpler approach: argparse.parse_args() already handles command-line
    # overrides correctly if arguments are defined with their final defaults.
    # The challenge is merging config file values *before* argparse applies
    # its defaults.

    # Let's go back to the strategy of:
    # 1. Define arguments with their final defaults using argparse.
    # 2. Add config and profile arguments.
    # 3. Parse all arguments using `parse_args()`. This gives us command-line
    #    values or argparse defaults.
    # 4. Load config file and profile.
    # 5. For each setting in the loaded config/profile, if the corresponding
    #    attribute in the *parsed args* still holds its *argparse default value*,
    #    then override it with the value from the config file (after type conversion).
    #    If the attribute in *parsed args* is different from its argparse default,
    #    it means the user provided it on the command line, and it should not be
    #    overridden by the config file.

    parser = argparse.ArgumentParser(description='Automatically analyze +45 protocols.')
    # Define arguments with their final default values
    arg_definitions = [
        ('--proto', {'default': 'scanner', 'help': 'Protocol to test'}),
        ('--host', {'default': "127.0.0.1", 'help': 'Host to test'}),
        ('--workdir', {'default': expanduser("~")+'/.legion/', 'help': 'Working directory'}),
        (('-p', '--port'), {'type': int, 'default': 0, 'help': 'Port where the protocol is listening'}),
        (('-i', '--intensity'), {'type': int, 'default': 2, 'help': 'Intensity level'}),
        (('-u', '--username'), {'default': "", 'help': 'Username for bruteforce'}),
        (('-U', '--ulist'), {'default': "", 'help': 'Usernames list for bruteforce'}),
        (('-k', '--password'), {'default': "", 'help': 'Password'}),
        (('-P', '--plist'), {'default': "", 'help': 'Passwords list for bruteforce'}),
        (('--protohelp',), {'action': "store_true", 'default': False, 'help': 'Set to get help of selected protocol'}),
        (('--notuse',), {'default': "", 'help': 'Comma separated tools to exclude'}),
        (('--extensions',), {'default': "html,txt,php,asp,aspx", 'help': 'USED IN HTTP/s: Set valid extensions'}),
        (('--path',), {'default': "", 'help': 'USED IN HTTP/s: Set the URL path'}),
        (('--ipv6',), {'default': "", 'help': 'USED IN HTTP/s: Used for reverse dns lookup with ipv6'}),
        (('--domain',), {'default': "", 'help': 'Set the domain name'}),
        (('--execonly',), {'default': "", 'help': 'Exec only this tool'}),
        (('-r', '--run'), {'action': "store_true", 'default': False, 'help': 'Just run the analysis'}),
        (('-v', '--verbose'), {'action': "store_true", 'default': True, 'help': 'Get output when the command finish'}),
        (('--config',), {'default': expanduser("~") + '/.legion/config.ini', 'help': 'Path to the configuration file'}),
        (('--profile',), {'default': 'DEFAULT', 'help': 'Profile to use from the configuration file'})
    ]

    # Add arguments to the parser, storing their default values
    arg_defaults = {}
    for names, kwargs in arg_definitions:
        action = parser.add_argument(*names, **kwargs)
        # Store the default value associated with the argument's destination
        arg_defaults[action.dest] = action.default

    # Parse command-line arguments - these take highest precedence
    args = parser.parse_args()

    config = configparser.ConfigParser()
    settings_from_config = {}

    # Read the configuration file if it exists
    if os.path.exists(args.config):
        config.read(args.config)

    # Load settings from DEFAULT or specified profile into a dictionary
    profile_name = args.profile
    if profile_name in config:
        settings_from_config.update(config.items(profile_name))
    elif 'DEFAULT' in config:
         settings_from_config.update(config.items('DEFAULT'))

    # Perform type conversions for settings loaded from the config file
    type_conversions = {
        'port': int,
        'intensity': int,
        'protohelp': lambda x: x.lower() == 'true',
        'run': lambda x: x.lower() == 'true',
        'verbose': lambda x: x.lower() == 'true',
        'notuse': lambda x: [item.strip() for item in x.split(',')] if x else [],
        'extensions': lambda x: [item.strip() for item in x.split(',')] if x else []
    }
    
    converted_settings_from_config = {}
    for key, value in settings_from_config.items():
        if key in type_conversions:
            try:
                converted_settings_from_config[key] = type_conversions[key](value)
            except ValueError:
                print(f"[!] Warning: Could not convert config value '{value}' for setting '{key}'. Skipping.")
        else:
            converted_settings_from_config[key] = value

    settings_from_config = converted_settings_from_config

    # Merge settings from config into the args Namespace
    # Only update args if the current value in args is the argparse default
    # (meaning it wasn't set on the command line).
    for key, value in settings_from_config.items():
        # Check if the attribute exists in the parsed args and if its current
        # value is the default value assigned by argparse.
        if hasattr(args, key) and getattr(args, key) == arg_defaults.get(key):
             setattr(args, key, value)
        # Special handling for boolean flags where default is False
        # If config sets a boolean flag to True, and the command line didn't set it,
        # update it. If command line set it (e.g., --protohelp is present), args.protohelp will be True,
        # which is not the default, so it won't be overridden.
        elif hasattr(args, key) and isinstance(arg_defaults.get(key), bool) and arg_defaults.get(key) is False and value is True:
             setattr(args, key, value)


    # Post-processing for list arguments that might still be strings if
    # provided via command line and not processed by the config conversion
    if isinstance(args.notuse, str):
        args.notuse = [item.strip() for item in args.notuse.split(',')] if args.notuse else []
    if isinstance(args.extensions, str):
         args.extensions = [item.strip() for item in args.extensions.split(',')] if args.extensions else []


    # Return the args Namespace object containing the final merged configuration
    return args

# Example of how the main function would use the returned args
# def main():
#     try:
#         config = parse_arguments()
        
#         # Now 'config' object contains settings from:
#         # 1. Command line (highest priority)
#         # 2. Config file profile
#         # 3. Config file DEFAULT section
#         # 4. Argparse default values (lowest priority)

#         # Proceed with setup and execution using the 'config' object
#         setup_environment(config)
        
#         if config.run: # Check the 'run' attribute from the merged config
#             run_analysis(config) # Pass the config object
#         else:
#             run_interactive_mode(config) # Pass the config object
            
#     except KeyboardInterrupt:
#         print("\n[!] Operation cancelled by user")
#         sys.exit(0)
#     except Exception as e:
#         print(f"[!] Fatal error: {str(e)}")
#         # Add a debug flag check from the config object
#         # if hasattr(config, 'debug') and config.debug:
#         #     import traceback
#         #     traceback.print_exc()
#         sys.exit(1)

# Note: The setup_environment, run_interactive_mode, and run_analysis functions
# would need to be updated to accept and use the 'config' object instead of
# individual arguments.

